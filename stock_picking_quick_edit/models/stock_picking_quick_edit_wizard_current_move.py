# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models
import openerp.addons.decimal_precision as dp


class StockPickingQuickEditWizardCurrentMove(models.TransientModel):
    _name = 'stock.picking.quick.edit.wizard.current.move'

    # Columns Section
    wizard_id = fields.Many2one(
        comodel_name='stock.picking.quick.edit.wizard', string='Wizard',
        select=True, ondelete='cascade')

    move_id = fields.Many2one(
        comodel_name='stock.move', string='Existing Move',
        required=True, readonly=True)

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product',
        required=True, readonly=True)

    product_uom_id = fields.Many2one(
        comodel_name='product.uom', string='UoM',
        required=True, readonly=True)

    old_product_uom_qty = fields.Float(
        string='Previous Quantity', required=True, readonly=True,
        digits_compute=dp.get_precision('Product UoS'))

    product_uom_qty = fields.Float(
        string='New Quantity', required=True,
        digits_compute=dp.get_precision('Product UoS'))
