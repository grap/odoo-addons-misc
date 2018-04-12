# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import os
import logging
from datetime import datetime

from openerp import api, fields, models, tools
from openerp.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)

try:
    from ftplib import FTP
except ImportError:
    _logger.warning(
        "Cannot import 'ftplib' Python Librairy. 'product_to_scale_bizerba'"
        " module will not work properly.")


class ProductScaleLog(models.Model):
    _name = 'product.scale.log'
    _inherit = 'ir.needaction_mixin'
    _order = 'log_date desc, id desc'

    _EXTERNAL_SIZE_ID_RIGHT = 4

    _ACTION_SELECTION = [
        ('create', 'Creation'),
        ('write', 'Update'),
        ('unlink', 'Deletion'),
    ]

    _ACTION_MAPPING = {
        'create': 'C',
        'write': 'C',
        'unlink': 'S',
    }

    _ENCODING_MAPPING = {
        'iso-8859-1': '\r\n',
    }

    _DELIMITER = '#'

    _EXTERNAL_TEXT_ACTION_CODE = 'C'

    _EXTERNAL_TEXT_DELIMITER = '#'

    _SCREEN_TEXT_DELIMITER = '#'

    # Column Section
    log_date = fields.Datetime(
        string='Log Date', required=True, readonly=True, select=True)

    scale_group_id = fields.Many2one(
        comodel_name='product.scale.group', string='Scale Group',
        required=True, readonly=True)

    scale_system_id = fields.Many2one(
        comodel_name='product.scale.system',
        string='Scale System', required=True, readonly=True)

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', readonly=True)

    screen_text = fields.Text(string='Screen Text', readonly=True)

    screen_text_display = fields.Text(
        string='Screen Text (Display)', readonly=True)

    product_text = fields.Text(
        compute='_compute_texts', string='Product Text', multi='texts',
        store=True)

    external_text = fields.Text(
        compute='_compute_texts', string='External Text', multi='texts',
        store=True)

    external_text_display = fields.Text(
        compute='_compute_texts', string='External Text (Display)',
        multi='texts', store=True)

    action = fields.Selection(
        selection=_ACTION_SELECTION, string='Action', required=True,
        readonly=True)

    sent = fields.Boolean(string='Is Sent', readonly=True, select=True)

    last_send_date = fields.Datetime('Last Send Date', readonly=True)

    company_id = fields.Many2one(
        comodel_name='res.company', related='scale_system_id.company_id',
        store=True, string='Company', readonly='True')

    # Compute Section
    @api.multi
    @api.depends('scale_system_id', 'product_id')
    def _compute_texts(self):
        for log in self:

            group = log.product_id.scale_group_id
            product_text =\
                self._ACTION_MAPPING[log.action] + self._DELIMITER
            external_texts = []

            # Set custom fields
            for product_line in group.scale_system_id.product_line_ids:
                if product_line.field_id:
                    value = getattr(log.product_id, product_line.field_id.name)

                if product_line.type == 'id':
                    product_text += str(log.product_id.external_id_bizerba)

                elif product_line.type == 'numeric':
                    value = tools.float_round(
                        value * product_line.numeric_coefficient,
                        precision_rounding=product_line.numeric_round)
                    product_text += str(value).replace('.0', '')

                elif product_line.type == 'text':
                    product_text += self._clean_value(value, product_line)

                elif product_line.type == 'external_text':
                    external_id = str(log.product_id.id)\
                        + str(product_line.id).rjust(
                            self._EXTERNAL_SIZE_ID_RIGHT, '0')
                    external_texts.append(log._generate_external_text(
                        value, product_line, external_id))
                    product_text += external_id

                elif product_line.type == 'constant':
                    product_text += self._clean_value(
                        product_line.constant_value, product_line)

                elif product_line.type == 'external_constant':
                    # Constant Value are like product ID = 0
                    external_id = str(product_line.id)

                    external_texts.append(log._generate_external_text(
                        product_line.constant_value, product_line,
                        external_id))
                    product_text += external_id

                elif product_line.type == 'many2one':
                    # If the many2one is defined
                    if value and not product_line.related_field_id:
                        product_text += value.id
                    elif value and product_line.related_field_id:
                        item_value = getattr(
                            value, product_line.related_field_id.name)
                        product_text +=\
                            item_value and str(item_value) or ''

                elif product_line.type == 'many2many':
                    # Select one value, depending of x2many_range
                    if product_line.x2many_range < len(value):
                        item = value[product_line.x2many_range - 1]
                        if product_line.related_field_id:
                            item_value = getattr(
                                item, product_line.related_field_id.name)
                        else:
                            item_value = str(item.id)
                        product_text += self._clean_value(
                            item_value, product_line)

                elif product_line.type == 'product_image':
                    product_text += self._generate_image_file_name(
                        log.product_id, product_line.field_id)

                if product_line.delimiter:
                    product_text += product_line.delimiter
            break_line = self._ENCODING_MAPPING[log.scale_system_id.encoding]

            log.product_text = product_text + break_line
            log.external_text = break_line.join(external_texts) + break_line
            log.external_text_display = '\n'.join(
                    [x.replace('\n', '') for x in external_texts])

    # Private Section
    @api.model
    def _clean_value(self, value, product_line):
        if not value:
            return ''
        elif product_line.multiline_length:
            res = ''
            current_val = value
            while current_val:
                res += current_val[:product_line.multiline_length]
                current_val = current_val[product_line.multiline_length:]
                if current_val:
                    res += product_line.multiline_separator
        else:
            res = value
        if product_line.delimiter:
            return res.replace(product_line.delimiter, '')
        else:
            return res

    @api.multi
    def _generate_external_text(self, value, product_line, external_id):
        self.ensure_one()
        external_text_list = [
            self._EXTERNAL_TEXT_ACTION_CODE,                    # WALO Code
            self.product_id.scale_group_id.external_shelf_id,   # ABNR Code
            external_id,                                        # TXNR Code
            self._clean_value(value, product_line),             # TEXT Code
        ]
        return self._EXTERNAL_TEXT_DELIMITER.join(external_text_list)

    @api.model
    def _generate_screen_texts(self, scale_group):
        product_obj = self.pool['product.product']
        lines = []

        products = product_obj.search(
            [('scale_group_id', '=', scale_group.id)],
            order='name', limit=scale_group.screen_product_qty)
        position = scale_group.screen_offset
        # Add products
        for product in products:
            lines.append(str(self._SCREEN_TEXT_DELIMITER.join([
                str(position),                              # KEYNUM Code
                scale_group.external_shelf_id,              # TSAB Code
                str(product.external_id_bizerba),           # TSDA Code
            ])))
            position += 1
        initial_position = position
        for x in range(
                initial_position, scale_group.last_product_position + 1):
            lines.append(str(self._SCREEN_TEXT_DELIMITER.join([
                str(position),                              # KEYNUM Code
                scale_group.external_shelf_id,              # TSAB Code
                '0',                                        # TSDA Code
            ])))
            position += 1
        return lines

    @api.model
    def _generate_image_file_name(self, obj, field):
        if getattr(obj, field.name):
            model_name = obj._model._name.replace('.', '_')
            extension = '.PNG'
            return "%s__%s__%d%s" % (model_name, field.name, obj.id, extension)
        else:
            return ''

    # View Section
    @api.model
    def _needaction_count(self, domain=None, context=None):
        return len(self.search([('sent', '=', False)]))

    @api.model
    def ftp_connection_open(self, scale_system):
        """Return a new FTP connection with found parameters."""
        _logger.info("Trying to connect to ftp://%s@%s" % (
            scale_system.ftp_login, scale_system.ftp_url))
        try:
            ftp = FTP(scale_system.ftp_url)
            if scale_system.ftp_login:
                ftp.login(
                    scale_system.ftp_login,
                    scale_system.ftp_password)
            else:
                ftp.login()
            return ftp
        except:
            raise UserError(
                "Connection to ftp://%s@%s failed." % (
                    scale_system.ftp_login, scale_system.ftp_url))

    @api.model
    def ftp_connection_close(self, ftp):
        try:
            ftp.quit()
        except:
            _logger.warning("Connection to ftp has not been properly closed")

    @api.model
    def ftp_connection_push_text_file(
            self, ftp, distant_folder_path, local_folder_path,
            pattern, lines, encoding):
        if lines:
            # Generate temporary text file
            f_name = datetime.now().strftime(pattern)
            local_path = os.path.join(local_folder_path, f_name)
            distant_path = os.path.join(distant_folder_path, f_name)
            f = open(local_path, 'w')
            for line in lines:
                f.write(line.encode(encoding))
            f.close()

            # Send File by FTP
            f = open(local_path, 'r')
            try:
                ftp.storbinary('STOR ' + distant_path, f)
            except:
                raise UserError(
                    "Unable to push the file %s on the FTP server.\n"
                    "Possible reasons :\n"
                    " * Incorrect access right for the current FTP user\n"
                    " * Distant folder '%s' doesn't exist" % (
                        f_name, distant_folder_path, ))

            # Delete temporary file
            os.remove(local_path)

    @api.model
    def ftp_connection_push_image_file(
            self, ftp, distant_folder_path, local_folder_path,
            obj, field):

        # Generate temporary image file
        f_name = self._generate_image_file_name(obj, field)
        if not f_name:
            # No image define
            return False
        local_path = os.path.join(local_folder_path, f_name)
        distant_path = os.path.join(distant_folder_path, f_name)
        image_base64 = getattr(obj, field.name)
        # Resize and save image
        tools.image_resize_image(
            base64_source=image_base64, size=(120, 120), encoding='base64',
            filetype='PNG')
        image_data = base64.b64decode(image_base64)
        f = open(local_path, 'wb')
        f.write(image_data)
        f.close()

        # Send File by FTP
        f = open(local_path, 'r')
        ftp.storbinary('STOR ' + distant_path, f)

        # Delete temporary file
        os.remove(local_path)

    @api.multi
    def send_log(self):
        if not len(self):
            return True

        scale_group_obj = self.env['product.scale.group']
        config_obj = self.env['ir.config_parameter']
        folder_path = config_obj.get_param('bizerba.local_folder_path')

        log_group_ids = {}
        order_logs = self.search(
            [('id', 'in', self.ids)], order='log_date desc')

        for log in order_logs:
            if log.scale_group_id.id not in log_group_ids.keys() and\
                    log.scale_group_id.screen_obsolete:
                log_group_ids[log.scale_group_id.id] = log.id

        for group_id, log_id in log_group_ids.iteritems():
            group = scale_group_obj.browse(group_id)
            log = self.browse(log_id)
            break_line =\
                self._ENCODING_MAPPING[group.scale_system_id.encoding]
            screen_texts = self._generate_screen_texts(group)
            screen_text = break_line.join(screen_texts) + break_line
            screen_text_display = '\n'.join(
                [x.replace('\n', '') for x in screen_texts])

            log.write({
                'screen_text': screen_text,
                'screen_text_display': screen_text_display,
            })
            group.write({
                'screen_obsolete': False,
            })

        system_map = {}
        for log in self:
            if log.scale_system_id in system_map.keys():
                system_map[log.scale_system_id].append(log)
            else:
                system_map[log.scale_system_id] = [log]

        for scale_system, logs in system_map.iteritems():

            # Open FTP Connection
            ftp = self.ftp_connection_open(logs[0].scale_system_id)
            if not ftp:
                return False

            # Generate and Send Files
            now = datetime.now()
            product_text_lst = []
            external_text_lst = []
            screen_text_lst = []

            for log in logs:
                if log.product_text:
                    product_text_lst.append(log.product_text)
                if log.external_text:
                    external_text_lst.append(log.external_text)
                if log.screen_text:
                    screen_text_lst.append(log.screen_text)

            # Push First Image for constrains reason
            for product_line in scale_system.product_line_ids:
                for log in logs:
                    if product_line.type == 'product_image':
                        # send product image
                        self.ftp_connection_push_image_file(
                            ftp, scale_system.product_image_relative_path,
                            folder_path, log.product_id, product_line.field_id)

            # Push First External Text for constrains reason
            if external_text_lst:
                self.ftp_connection_push_text_file(
                    ftp, scale_system.csv_relative_path, folder_path,
                    scale_system.external_text_file_pattern,
                    external_text_lst, scale_system.encoding)

            # Push Product list
            if product_text_lst:
                self.ftp_connection_push_text_file(
                    ftp, scale_system.csv_relative_path, folder_path,
                    scale_system.product_text_file_pattern,
                    product_text_lst, scale_system.encoding)

            # Push Screen display
            if screen_text_lst:
                self.ftp_connection_push_text_file(
                    ftp, scale_system.csv_relative_path, folder_path,
                    scale_system.screen_text_file_pattern,
                    screen_text_lst, scale_system.encoding)

            # Close FTP Connection
            self.ftp_connection_close(ftp)

            # Mark logs as sent
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logs.write({
                'sent': True,
                'last_send_date': now,
                })

    @api.model
    def cron_send_to_scale(self):
        logs = self.search([('sent', '=', False)], order='log_date')
        logs.send_log()

    @api.model
    def cron_send_to_scale_per_system(self, scale_system_id):
        logs = self.search(
            [('sent', '=', False), ('scale_system_id', '=', scale_system_id)],
            order='log_date')
        logs.send_log()
