# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class StockPickingQuickEditWizardNewMove(models.TransientModel):
    _name = 'stock.picking.quick.edit.wizard.new.move'

    # Columns Section
    wizard_id = fields.Many2one(
        comodel_name='stock.picking.quick.edit.wizard', string='Wizard',
        select=True, ondelete='cascade')

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', required=True)

    product_uom_qty = fields.Float(
        string='Quantity', required=True,
        digits_compute=dp.get_precision('Product UoS'))

    product_uom_id = fields.Many2one(
        comodel_name='product.uom', string='UoM', readonly=True)

    # Onchange section
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_uom_qty = 1
            self.product_uom_id = self.product_id.uom_id.id
        else:
            self.product_uom_qty = 0
            self.product_uom_id = False

    @api.multi
    def prepare_stock_move(self):
        self.ensure_one()
        move_obj = self.env['stock.move']
        picking = self.wizard_id.picking_id
        res = {
            'name': '[%s] %s' % (
                self.product_id.code, self.product_id.name),
            'date_expected': picking.min_date,
            'company_id': picking.company_id.id,
            'picking_id': picking.id,
            'product_id': self.product_id.id,
            'product_uom_qty': self.product_uom_qty,
            'product_uos_qty': self.product_uom_qty,
            'product_uom': self.product_id.uom_id.id,
        }
        # Handle lazely stock_account compatibility
        if 'invoice_state' in move_obj._fields:
            res.update({'invoice_state': picking.invoice_state})
        return res
