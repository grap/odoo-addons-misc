# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class StockPickingQuickEditWizard(models.TransientModel):
    _name = 'stock.picking.quick.edit.wizard'

    picking_id = fields.Many2one(
        comodel_name='stock.picking', string='Delivery Order', readonly=True,
        required=True, default=lambda s: s._default_picking_id())

    current_move_ids = fields.One2many(
        comodel_name='stock.picking.quick.edit.wizard.current.move',
        inverse_name='wizard_id', string='Existing Moves',
        default=lambda s: s._default_current_move_ids())

    new_move_ids = fields.One2many(
        comodel_name='stock.picking.quick.edit.wizard.new.move',
        inverse_name='wizard_id', string='New Moves')

    # Default Section
    def _default_picking_id(self):
        return self.env.context.get('active_id', False)

    def _default_current_move_ids(self):
        res = []
        picking_obj = self.env['stock.picking']
        current_picking = picking_obj.browse(self._default_picking_id())
        for move in current_picking.move_lines:
            res.append((0, 0, {
                'move_id': move.id,
                'product_id': move.product_id.id,
                'product_uom_qty': move.product_uom_qty,
                'product_uom_id': move.product_uom.id,
            }))
        return res

    @api.multi
    def apply(self):
        self.ensure_one()
        move_obj = self.env['stock.move']
        picking = self.picking_id

        # Manage move changes
        for move in picking.move_lines:
            current_move = self.current_move_ids.filtered(
                lambda x: x.move_id== move)
            if current_move:
                # Update Value
                product_uos_qty = move.onchange_quantity(
                    move.product_id.id,
                    current_move.product_uom_qty, move.product_uom.id,
                    move.product_uos.id)['value']['product_uos_qty']
                move_vals = {
                    'product_uom_qty': current_move.product_uom_qty,
                    'product_uos_qty': product_uos_qty,
                }
            else:
                # If not found, the row has been deleted by the user
                # We set quantity to 0
                move_vals = {
                    'product_uom_qty': 0,
                    'product_uos_qty': 0,
                }
            move.write(move_vals)

        # Manage move creations
        if self.new_move_ids:
            created_moves = []
            location_src_ids = self.mapped('picking_id.move_lines.location_id')
            location_dest_ids = self.mapped(
                'picking_id.move_lines.location_dest_id')
            move_states = list(set(self.mapped('picking_id.move_lines.state')))
            # if move_obj._fields.
            if len(location_src_ids) != 1 or len(location_dest_ids) != 1:
                raise UserError(_(
                    "Unable to quick add new lines to a"
                    " picking with stock moves in different locations"))
            if len(move_states) != 1:
                raise UserError(_(
                    "Unable to quick add new lines to a"
                    " picking with stock moves in different states\n %s") % (
                        ', '.join(move_states)))

            for new_move in self.new_move_ids:
                move_vals = new_move.prepare_stock_move()
                move_vals.update({
                    'location_id': location_src_ids[0].id,
                    'location_dest_id': location_dest_ids[0].id,
                })
                created_moves.append(move_obj.create(move_vals))

            if move_states[0] != 'draft':
                for created_move in created_moves:
                    created_move.action_confirm()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
