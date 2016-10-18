# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model

# _logger = logging.getLogger(__name__)
# try:
#     import ftplib
# except ImportError:
#     _logger.info("Cannot import 'ftplib' Python Librairy.")


class product_scale_log(Model):
    _name = 'product.scale.log'
    _inherit = 'ir.needaction_mixin'
    _order = 'log_date desc, id desc'

    _EXTERNAL_ID_PRODUCT_SIZE = 8

    _EXTERNAL_SIZE_ID_RIGHT = 6

    _DELIMITER = '#'

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

    _EXTERNAL_TEXT_ACTION_CODE = 'C'

    _EXTERNAL_TEXT_DELIMITER = '#'

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
        return str(res).replace(product_line.delimiter, '')

    def _generate_external_text(self, value, product_line, external_id, log):
        # TODO: IMPROVE ME. Some hardcoded design
        external_text_list = [
            self._EXTERNAL_TEXT_ACTION_CODE,                    # WALO Code
            log.product_id.scale_group_id.external_identity,    # ABNR Code
            external_id,                                        # TXNR Code
            self._clean_value(value, product_line),             # TEXT Code
            '',
        ]
        return self._EXTERNAL_TEXT_DELIMITER.join(external_text_list)

    # Compute Section
    def _compute_action_code(
            self, cr, uid, ids, field_names, arg=None, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context=context):
            res[log.id] = self._ACTION_MAPPING[log.action]
        return res

    def _compute_text(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for log in self.browse(cr, uid, ids, context):

            group = log.product_id.scale_group_id
            product_text = log.action_code + self._DELIMITER
            external_texts = []

            # Set custom fields
            for product_line in group.scale_system_id.product_line_ids:
                if product_line.field_id:
                    value = getattr(log.product_id, product_line.field_id.name)

                if product_line.type == 'id':
                    product_text += str(log.product_id.id)

                elif product_line.type == 'numeric':
                    value = tools.float_round(
                        value * product_line.numeric_coefficient,
                        precision_rounding=product_line.numeric_round)
                    product_text += str(value).replace('.0', '')

                elif product_line.type == 'text':
                    product_text += self._clean_value(value, product_line)

                elif product_line.type == 'external_text':
                    external_id = str(log.product_id.id) + str(product_line.id)
                    external_texts.append(self._generate_external_text(
                        value, product_line, external_id, log))
                    product_text += external_id

                elif product_line.type == 'constant':
                    product_text += self._clean_value(
                        product_line.constant_value, product_line)

                elif product_line.type == 'external_constant':
                    # Constant Value are like product ID = 0
                    external_id = str(product_line.id)
#                    product_text += self._clean_value(
#                        product_line.constant_value, product_line)

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
                            item_value = item.id
                        product_text += self._clean_value(
                            item_value, product_line)

                elif product_line.type == 'product_image':
                    product_text += str(log.product_id.id) +\
                        product_line.suffix

                product_text += product_line.delimiter
            res[log.id] = {
                'product_text': product_text,
                'external_text': '\n'.join(external_texts),
                'external_text_display': '\n'.join(
                    [x.replace('\n', '') for x in external_texts]),
            }
        return res

    # Column Section
    _columns = {
        'log_date': fields.datetime('Log Date', required=True),
        'scale_system_id': fields.many2one(
            'product.scale.system', string='Scale System', required=True),
        'product_id': fields.many2one(
            'product.product', string='Product'),
        'product_text': fields.function(
            _compute_text, type='text', string='Product Text',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None:
                    ids, ['scale_system_id', 'product_id'], 10)}),
        'external_text': fields.function(
            _compute_text, type='text', string='External Text',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None: ids, [
                    'scale_system_id', 'product_id', 'product_id'], 10)}),
        'external_text_display': fields.function(
            _compute_text, type='text', string='External Text (Display)',
            multi='compute_text', store={'product.scale.log': (
                lambda self, cr, uid, ids, context=None: ids, [
                    'scale_system_id', 'product_id', 'product_id'], 10)}),
        'action': fields.selection(
            _ACTION_SELECTION, string='Action', required=True),
        'action_code': fields.function(
            _compute_action_code, string='Action Code'),
        'sent': fields.boolean(string='Is Sent'),
    }

    # View Section
    def _needaction_count(self, cr, uid, domain=None, context=None):
        return len(
            self.search(cr, uid, [('sent', '=', False)], context=context))

#    # Custom Section
#    def ftp_connection_open(self, cr, uid, log, context=None):
#        """Return a new FTP connection with found parameters."""
#        _logger.info("Trying to connect to ftp://%s@%s" % (
#            log.scale_system_id.ftp_login, log.scale_system_id.ftp_password))
#        # TODO Try Catch me
#        ftp = FTP(log.scale_system_id.ftp_url)
#        if log.scale_system_id.ftp_login:
#            ftp.login(
#                log.scale_system_id.ftp_login,
#                log.scale_system_id.ftp_password)
#        else:
#            ftp.login()
#        return ftp

#    def ftp_connection_close(self, cr, uid, ftp, context=None):
#        _logger.info("Trying to disconnect from ftp://%s@%s" % (ftp.host)
#        ftp.quit()

#    def ftp_connection_push_text_file(
#            self, cr, uid, ftp, directory, pattern, lines, context=None):
#        ftp.dir(directory)
#        # Make temporary File
#        # TODO
#        text_file = open('myfile', 'w')
#        # Delete Temporary File
#        # TODO
#        ftp.dir('/')

    def send_log(self, cr, uid, context=None):
        log_ids = self.search(
            cr, uid, [('sent', '=', False)], order='log_date', context=context)
        for log in self.browse(cr, uid, log_ids, context=context):
            # TODO
            # GROUP BY scale_system_id
            # First Push Images
            # Send data to the correct FTP, based on scale_system_id
            # Clean attachment, once managed
            self.write(cr, uid, [log.id], {'sent': True}, context=context)
