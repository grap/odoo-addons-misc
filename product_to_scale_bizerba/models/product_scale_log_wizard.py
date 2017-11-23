# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class ProductScaleLogWizard(orm.TransientModel):
    _name = 'product.scale.log.wizard'

    _LOG_TYPE_SELECTION = [
        ('create', 'Create'),
        ('write', 'Update'),
        ('unlink', 'Unlink'),
    ]

    # Column Section
    _columns = {
        'product_qty': fields.integer(
            string='Product Quantity', readonly=True),
        'log_type': fields.selection(
            _LOG_TYPE_SELECTION, string='Log Type', required=True),
    }

    # Default Section
    def _default_product_qty(self, cr, uid, context=None):
        return len(context.get('active_ids', []))

    _defaults = {
        'product_qty': _default_product_qty,
        'log_type': 'create',
    }

    def send_log(self, cr, uid, ids, context=None):
        product_obj = self.pool['product.product']
        for wizard in self.browse(cr, uid, ids, context=context):
            product_ids = product_obj.search(cr, uid, [
                ('id', 'in', context.get('active_ids', [])),
                ('scale_group_id', '!=', False),
            ], context=context)
            if wizard.log_type == 'create':
                product_obj.send_scale_create(
                    cr, uid, product_ids, context=context)
            elif wizard.log_type == 'write':
                product_obj.send_scale_write(
                    cr, uid, product_ids, context=context)
            elif wizard.log_type == 'unlink':
                product_obj.send_scale_unlink(
                    cr, uid, product_ids, context=context)
        return True
