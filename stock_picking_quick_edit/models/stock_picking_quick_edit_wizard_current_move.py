# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class StockPickingQuickEditWizardCurrentMove(orm.TransientModel):
    _name = 'stock.picking.quick.edit.wizard.current.move'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'stock.picking.quick.edit.wizard', 'Wizard',
            select=True),
        'move_id': fields.many2one(
            'stock.move', 'Existing Move', required=True, readonly=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True, readonly=True),
        'product_uom_qty': fields.float(
            'Quantity', required=True),
        'product_uom_id': fields.many2one(
            'product.uom', 'UoM', required=True, readonly=True),
    }
