# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.orm import TransientModel
from openerp.osv import fields
from openerp.osv.osv import except_osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class StockPickingMassChangeWizard(TransientModel):
    _name = 'stock.picking.mass.change.wizard'

    # Columns Section
    _columns = {
        'product_id': fields.many2one(
            'product.product', string='Product', required=True),
        'concerned_picking_qty': fields.integer(
            string='Concerned Picking Quantity', readonly=True),
        'ordered_product_qty': fields.float(
            string='Ordered Product Quantity', readonly=True,
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'target_product_qty': fields.float(
            string='Target Product Quantity', required=True,
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'computed_product_qty': fields.float(
            string='Computed Product Quantity', readonly=True,
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'change_method': fields.selection([
            ('fifo', 'First In First Served'),
            ('pro_rata', 'Pro Rata'),
        ], string='Change Method', required=True),
        'rounding': fields.float(
            string='Rounding', required=True,
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'picking_qty': fields.integer(
            string='Selected Picking Qty', readonly=True),
        'line_ids': fields.one2many(
            'stock.picking.mass.change.wizard.line', 'wizard_id',
            string='Lines'),
    }

    # Default Section
    def _default_picking_qty(self, cr, uid, context=None):
        if context.get('active_ids'):
            return len(context.get('active_ids'))
        else:
            return 0

    _defaults = {
        'change_method': 'pro_rata',
        'picking_qty': _default_picking_qty,
    }

    # On Change Section
    def onchange_product_id(
            self, cr, uid, ids, product_id, context=None):
        spo_obj = self.pool['stock.picking']
        pp_obj = self.pool['product.product']
        ordered_product_qty = 0
        concerned_picking_qty = 0
        line_ids = []
        rounding = 1
        picking_ids = context.get('active_ids', [])
        if product_id:
            rounding = pp_obj.browse(
                cr, uid, product_id, context=context).uom_id.rounding
            for picking in spo_obj.browse(
                    cr, uid, picking_ids, context=context):
                concerned_picking = False
                for move in picking.move_lines:
                    if move.product_id.id == product_id:
                        concerned_picking = True
                        ordered_product_qty += move.product_qty
                        line_ids.append((0, 0, {
                            'move_id': move.id,
                            'picking_id': picking.id,
                            'sale_id': picking.sale_id.id,
                            'partner_id': picking.partner_id.id,
                            'ordered_qty': move.product_qty,
                            'exact_target_qty': 0,
                            'target_qty': 0,
                        }))
                if concerned_picking:
                    concerned_picking_qty += 1
        return {'value': {
            'rounding': rounding,
            'concerned_picking_qty': concerned_picking_qty,
            'ordered_product_qty': ordered_product_qty,
            'line_ids': line_ids,
        }}

    def onchange_change_setting(
            self, cr, uid, ids, product_id, rounding, ordered_product_qty,
            change_method, target_product_qty, context=None):
        spo_obj = self.pool['stock.picking']
        computed_product_qty = 0
        line_ids = []

        picking_ids = context.get('active_ids', [])
        if product_id and ordered_product_qty != 0:
            for picking in spo_obj.browse(
                    cr, uid, picking_ids, context=context):
                for move in picking.move_lines:
                    if move.product_id.id == product_id:
                        exact_target_qty = self._compute_exact_target_qty(
                            ordered_product_qty, change_method,
                            target_product_qty, move.product_qty)
                        target_qty = self._round_value(
                            exact_target_qty, rounding)
                        line_ids.append((0, 0, {
                            'picking_id': picking.id,
                            'move_id': move.id,
                            'sale_id': picking.sale_id.id,
                            'partner_id': picking.partner_id.id,
                            'ordered_qty': move.product_qty,
                            'exact_target_qty': exact_target_qty,
                            'target_qty': target_qty,
                        }))
                        computed_product_qty += target_qty
        return {'value': {
            'computed_product_qty': computed_product_qty,
            'line_ids': line_ids,
        }}

    # Custom Section
    def _compute_exact_target_qty(
            self, ordered_product_qty, change_method, target_product_qty, qty):
        if change_method != 'pro_rata':
            raise except_osv(
                _('Not Implemented!'),
                _('Not Implemented feature'))
        else:
            return qty / ordered_product_qty * target_product_qty

    def _round_value(self, value, rounding):
            under = (value // rounding) * rounding
            over = ((value // rounding) * rounding) + rounding
            return (over - value <= value - under) and over or under

    # Button Section
    def mass_change_confirm(self, cr, uid, ids, context=None):
        sm_obj = self.pool['stock.move']
        for wizard in self.browse(cr, uid, ids, context=context):
            for line in wizard.line_ids:
                product_uos_qty = sm_obj.onchange_quantity(
                    cr, uid, [line.move_id.id], wizard.product_id.id,
                    line.target_qty, line.move_id.product_uom.id,
                    line.move_id.product_uos.id)['value']['product_uos_qty']
                sm_obj.write(cr, uid, [line.move_id.id], {
                    'name': line.move_id.name + ' (%s -> %s)' % (
                        line.move_id.product_qty, line.target_qty),
                    'product_uom_qty': line.target_qty,
                    'product_uos_qty': product_uos_qty,
                }, context=context)
        return True
