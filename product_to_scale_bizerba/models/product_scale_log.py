# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import os
import logging
from datetime import datetime

from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import except_orm
from openerp.tools import image_resize_image
from openerp.osv.orm import Model

_logger = logging.getLogger(__name__)

try:
    from ftplib import FTP
except ImportError:
    _logger.warning(
        "Cannot import 'ftplib' Python Librairy. 'product_to_scale_bizerba'"
        " module will not work properly.")


class product_scale_log(Model):
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

    # Private Section
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

    def _generate_external_text(self, value, product_line, external_id, log):
        external_text_list = [
            self._EXTERNAL_TEXT_ACTION_CODE,                    # WALO Code
            log.product_id.scale_group_id.external_shelf_id,    # ABNR Code
            external_id,                                        # TXNR Code
            self._clean_value(value, product_line),             # TEXT Code
        ]
        return self._EXTERNAL_TEXT_DELIMITER.join(external_text_list)

    def _generate_screen_texts(self, cr, uid, scale_group, context=None):
        product_obj = self.pool['product.product']
        lines = []

        product_ids = product_obj.search(
            cr, uid, [('scale_group_id', '=', scale_group.id)],
            order='name', limit=scale_group.screen_product_qty,
            context=context)
        position = scale_group.screen_offset
        # Add products
        for product in product_obj.browse(
                cr, uid, product_ids, context=context):
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

    # Compute Section
    def _compute_text(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context):

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
                    external_texts.append(self._generate_external_text(
                        value, product_line, external_id, log))
                    product_text += external_id

                elif product_line.type == 'constant':
                    product_text += self._clean_value(
                        product_line.constant_value, product_line)

                elif product_line.type == 'external_constant':
                    # Constant Value are like product ID = 0
                    external_id = str(product_line.id)

                    external_texts.append(self._generate_external_text(
                        product_line.constant_value, product_line, external_id,
                        log))
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
                        cr, uid, log.product_id, product_line.field_id,
                        context=context)

                if product_line.delimiter:
                    product_text += product_line.delimiter
            break_line = self._ENCODING_MAPPING[log.scale_system_id.encoding]

            res[log.id] = {
                'product_text': product_text + break_line,
                'external_text': break_line.join(external_texts) + break_line,
                'external_text_display': '\n'.join(
                    [x.replace('\n', '') for x in external_texts]),
            }
        return res

    # Column Section
    _columns = {
        'log_date': fields.datetime('Log Date', required=True, readonly=True),

        'scale_group_id': fields.many2one(
            'product.scale.group', string='Scale Group', required=True,
            readonly=True),

        'scale_system_id': fields.many2one(
            'product.scale.system', string='Scale System', required=True,
            readonly=True),

        'product_id': fields.many2one(
            'product.product', string='Product', readonly=True),

        'screen_text': fields.text(
            string='Screen Text', readonly=True),

        'screen_text_display': fields.text(
            string='Screen Text (Display)', readonly=True),

        'product_text': fields.function(
            _compute_text, type='text', string='Product Text',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'product_id'], 10)}),

        'external_text': fields.function(
            _compute_text, type='text', string='External Text',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'product_id'], 10)}),

        'external_text_display': fields.function(
            _compute_text, type='text', string='External Text (Display)',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'product_id'], 10)}),

        'action': fields.selection(
            _ACTION_SELECTION, string='Action', required=True, readonly=True),

        'sent': fields.boolean(string='Is Sent', readonly=True),

        'last_send_date': fields.datetime('Last Send Date', readonly=True),

        'company_id': fields.related(
            'scale_system_id', 'company_id', type='many2one', store=True,
            relation='res.company', string='Company', readonly='True'),
    }

    # View Section
    def _needaction_count(self, cr, uid, domain=None, context=None):
        return len(
            self.search(cr, uid, [('sent', '=', False)], context=context))

    def ftp_connection_open(self, cr, uid, scale_system, context=None):
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
            raise except_orm(
                "Connexion Error",
                "Connection to ftp://%s@%s failed." % (
                    scale_system.ftp_login, scale_system.ftp_url))

    def ftp_connection_close(self, cr, uid, ftp, context=None):
        try:
            ftp.quit()
        except:
            _logger.warning("Connection to ftp has not been properly closed")

    def ftp_connection_push_text_file(
            self, cr, uid, ftp, distant_folder_path, local_folder_path,
            pattern, lines, encoding, context=None):
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
                raise except_orm(
                    "Write Error!",
                    "Unable to push the file %s on the FTP server.\n"
                    "Possible reasons :\n"
                    " * Incorrect access right for the current FTP user\n"
                    " * Distant folder '%s' doesn't exist" % (
                        f_name, distant_folder_path, ))

            # Delete temporary file
            os.remove(local_path)

    def ftp_connection_push_image_file(
            self, cr, uid, ftp, distant_folder_path, local_folder_path,
            obj, field, context=None):

        # Generate temporary image file
        f_name = self._generate_image_file_name(
            cr, uid, obj, field, context=context)
        if not f_name:
            # No image define
            return False
        local_path = os.path.join(local_folder_path, f_name)
        distant_path = os.path.join(distant_folder_path, f_name)
        image_base64 = getattr(obj, field.name)
        # Resize and save image
        image_resize_image(
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

    def _generate_image_file_name(self, cr, uid, obj, field, context=None):
        if getattr(obj, field.name):
            model_name = obj._model._name.replace('.', '_')
            extension = '.PNG'
            return "%s__%s__%d%s" % (model_name, field.name, obj.id, extension)
        else:
            return ''

    def send_log(self, cr, uid, ids, context=None):
        if not ids:
            return True

        scale_group_obj = self.pool['product.scale.group']
        config_obj = self.pool['ir.config_parameter']
        folder_path = config_obj.get_param(
            cr, uid, 'bizerba.local_folder_path', context=context)

        log_group_ids = {}
        order_log_ids = self.search(
            cr, uid, [('id', 'in', ids)], order='log_date desc',
            context=context)

        for log in self.browse(cr, uid, order_log_ids, context=context):
            if log.scale_group_id.id not in log_group_ids.keys() and\
                    log.scale_group_id.screen_obsolete:
                log_group_ids[log.scale_group_id.id] = log.id

        for group_id, log_id in log_group_ids.iteritems():
            group = scale_group_obj.browse(cr, uid, group_id, context=context)
            break_line =\
                self._ENCODING_MAPPING[group.scale_system_id.encoding]
            screen_texts = self._generate_screen_texts(
                cr, uid, group, context=context)
            screen_text = break_line.join(screen_texts) + break_line
            screen_text_display = '\n'.join(
                [x.replace('\n', '') for x in screen_texts])

            self.write(cr, uid, [log_id], {
                'screen_text': screen_text,
                'screen_text_display': screen_text_display,
            }, context=context)
            scale_group_obj.write(cr, uid, [group_id], {
                'screen_obsolete': False,
            }, context=context)

        system_map = {}
        for log in self.browse(cr, uid, ids, context=context):
            if log.scale_system_id in system_map.keys():
                system_map[log.scale_system_id].append(log)
            else:
                system_map[log.scale_system_id] = [log]

        for scale_system, logs in system_map.iteritems():

            # Open FTP Connection
            ftp = self.ftp_connection_open(
                cr, uid, logs[0].scale_system_id, context=context)
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
                if product_line.type == 'product_image':
                    # send product image
                    self.ftp_connection_push_image_file(
                        cr, uid, ftp,
                        scale_system.product_image_relative_path,
                        folder_path, log.product_id,
                        product_line.field_id, context=context)

            # Push First External Text for constrains reason
            if external_text_lst:
                self.ftp_connection_push_text_file(
                    cr, uid, ftp, scale_system.csv_relative_path,
                    folder_path, scale_system.external_text_file_pattern,
                    external_text_lst, scale_system.encoding, context=context)

            # Push Product list
            if product_text_lst:
                self.ftp_connection_push_text_file(
                    cr, uid, ftp, scale_system.csv_relative_path,
                    folder_path, scale_system.product_text_file_pattern,
                    product_text_lst, scale_system.encoding, context=context)

            # Push Screen display
            if screen_text_lst:
                self.ftp_connection_push_text_file(
                    cr, uid, ftp, scale_system.csv_relative_path,
                    folder_path, scale_system.screen_text_file_pattern,
                    screen_text_lst, scale_system.encoding, context=context)

            # Close FTP Connection
            self.ftp_connection_close(cr, uid, ftp, context=context)

            # Mark logs as sent
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.write(
                cr, uid, [log.id for log in logs], {
                    'sent': True,
                    'last_send_date': now,
                }, context=context)
        return True

    def cron_send_to_scale(self, cr, uid, context=None):
        log_ids = self.search(
            cr, uid, [('sent', '=', False)], order='log_date', context=context)
        self.send_log(cr, uid, log_ids, context=context)
