# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Picking Quick Edit module for Odoo
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

from openerp.osv import orm, fields
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class StockPickingQuickEditWizard(orm.TransientModel):
    _name = 'stock.picking.quick.edit.wizard'

    _columns = {
        'picking_id': fields.many2one(
            'stock.picking', 'Delivery Order', readonly=True,
            required=True),
        'current_move_ids': fields.one2many(
            'stock.picking.quick.edit.wizard.current.move',
            'wizard_id', 'Existing Moves'),
        'new_move_ids': fields.one2many(
            'stock.picking.quick.edit.wizard.new.move',
            'wizard_id', 'New Moves'),
    }

    def _default_current_move_ids(self, cr, uid, context=None):
        res = []
        if context.get('active_id', False):
            sp_obj = self.pool['stock.picking']
            sp = sp_obj.browse(
                cr, uid, context.get('active_id'), context=context)
            for move in sp.move_lines:
                res.append((0, 0, {
                    'move_id': move.id,
                    'product_id': move.product_id.id,
                    'product_qty': move.product_qty,
                    'product_uom': move.product_uom.id,
                }))
        return res

    def _default_picking_id(self, cr, uid, context=None):
        return context.get('active_id', False)

    _defaults = {
        'picking_id': _default_picking_id,
        'current_move_ids': _default_current_move_ids,
    }

    def apply(self, cr, uid, ids, context=None):
        sm_obj = self.pool['stock.move']
        for wizard in self.browse(cr, uid, ids, context=context):
            picking = wizard.picking_id
            location_id = []
            location_dest_id = []
            new_sm_ids = []
            for sm in picking.move_lines:
                if sm.location_id.id not in location_id:
                    location_id.append(sm.location_id.id)
                if sm.location_dest_id.id not in location_dest_id:
                    location_dest_id.append(sm.location_dest_id.id)
                found = False
                for current_move in wizard.current_move_ids:
                    if current_move.move_id.id == sm.id:
                        product_uos_qty = sm_obj.onchange_quantity(
                            cr, uid, [sm.id], sm.product_id.id,
                            current_move.product_qty, sm.product_uom.id,
                            sm.product_uos.id)['value']['product_uos_qty']
                        sm_obj.write(cr, uid, [sm.id], {
                            'product_qty': current_move.product_qty,
                            'product_uos_qty': product_uos_qty,
                        }, context=context)
                        found = True
                # If not found, the row has been deleted by the user
                # We set quantity to 0
                if not found:
                    sm_obj.write(cr, uid, [sm.id], {
                        'product_qty': 0,
                        'product_uos_qty': 0,
                    }, context=context)

            if wizard.new_move_ids\
                    and (len(location_id) != 1 or len(location_dest_id) != 1):
                raise except_osv(
                    _('Error!'),
                    _("""Unable to quick edit a picking with stock moves"""
                        """ in different locations!"""))
            for new_move in wizard.new_move_ids:
                sm_id = sm_obj.create(cr, uid, {
                    'name': '[%s] %s' % (
                        new_move.product_id.code, new_move.product_id.name),
                    'date_expected': picking.min_date,
                    'company_id': picking.company_id.id,
                    'type': picking.type,
                    'picking_id': picking.id,
                    'product_id': new_move.product_id.id,
                    'product_qty': new_move.product_qty,
                    'product_uos_qty': new_move.product_qty,
                    'weight_uom_id': new_move.product_id.uom_id.id,
                    'product_uom': new_move.product_id.uom_id.id,
                    'location_id': location_id[0],
                    'location_dest_id': location_dest_id[0],
                }, context=context)
                new_sm_ids.append(sm_id)

            if new_sm_ids and picking.state == 'confirmed':
                sm_obj.action_confirm(cr, uid, new_sm_ids, context=context)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
