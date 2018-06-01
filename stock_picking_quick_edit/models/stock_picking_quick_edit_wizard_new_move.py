# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class StockPickingQuickEditWizardNewMove(orm.TransientModel):
    _name = 'stock.picking.quick.edit.wizard.new.move'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'stock.picking.quick.edit.wizard', 'Wizard',
            select=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True),
        'product_uom_qty': fields.float(
            'Quantity', required=True),
        'product_uom_id': fields.many2one(
            'product.uom', 'UoM', readonly=True),
    }

    # View Section
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        pp_obj = self.pool['product.product']
        if not product_id:
            return {
                'product_uom_qty': 0,
                'product_uom_id': False,
            }
        pp = pp_obj.browse(cr, uid, product_id, context=context)
        return {'value': {
            'product_uom_qty': 1.00,
            'product_uom_id': pp.uom_id.id,
        }}
