# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class StockPickingMassChangeWizardLine(models.TransientModel):
    _name = 'stock.picking.mass.change.wizard.line'

    # Columns Section
    wizard_id = fields.Many2one(
        comodel_name='stock.picking.mass.change.wizard', string='Wizard',
        ondelete='cascade', select=True)

    picking_id = fields.Many2one(
        comodel_name='stock.picking', string='Picking', required=True,
        readonly=True)

    picking_date = fields.Datetime(string='Picking Creation Date')

    move_id = fields.Many2one(
        comodel_name='stock.move', string='Move', required=True,
        readonly=True)

    origin = fields.Char(string='Source Document', readonly=True)

    ordered_qty = fields.Float(
        string='Ordered Qty', required=True, readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))

    exact_target_qty = fields.Float(
        string='Theoretical Target Qty', required=True, readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))

    target_qty = fields.Float(
        string='Target Qty', required=True,
        digits=dp.get_precision('Product Unit of Measure'))

    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner',
        readonly=True)

    @api.model
    def _prepare_from_stock_move(self, move):
        picking = move.picking_id
        return {
            'move_id': move.id,
            'picking_date': picking.date,
            'picking_id': picking.id,
            'origin': picking.origin,
            'partner_id': picking.partner_id.id,
            'ordered_qty': move.product_qty,
            'exact_target_qty': 0,
            'target_qty': 0,
        }
