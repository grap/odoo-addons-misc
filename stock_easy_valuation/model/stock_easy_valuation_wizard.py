# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Easy Valuation for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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

import time

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class stock_easy_valuation_wizard(TransientModel):
    _name = 'stock.easy.valuation.wizard'
    _rec_name = 'valuation_date'

    def compute(self, cr, uid, ids, context=None):
        # TODO FIXME Check if inventory_ids are correct:
        # -> must be after the valuation_date
        # -> must be validated
        pp_obj = self.pool['product.product']
        pc_obj = self.pool['product.category']
        si_obj = self.pool['stock.inventory']
        sevwpl_obj = self.pool['stock.easy.valuation.wizard.product.line']
        sevwcl_obj = self.pool['stock.easy.valuation.wizard.category.line']
        id = ids[0]
        sevw = self.browse(cr, uid, id, context=context)

        # Get all products (active or not)
        pp_ids = pp_obj.search(cr, uid, [
            '|', ('active', '=', False), ('active', '=', True)], order='name',
            context=context)

        # Get all Product Category (order by parent_left)
        pc_ids = pc_obj.search(
            cr, uid, [], order='parent_left', context=context)

        pc_res = {x: {'valuation': 0} for x in pc_ids}
        for pc_id in pc_ids:
            sevwcl_obj.create(cr, uid, {
                'wizard_id': sevw.id,
                'category_id': pc_id,
            }, context=context)

        # Compute Theoretical Quantity at requested date
        ctx = context.copy()
        ctx['compute_child'] = True
        ctx['to_date'] = sevw.valuation_date
        pp_res = pp_obj._product_available(
            cr, uid, pp_ids, ['qty_available'], context=ctx)
        for k, v in pp_res.items():
            pp_res[k]['qty_variation'] = 0

        # Compute variation due to inventories realized after the requested
        # date
        inventory_ids = [x.id for x in sevw.inventory_ids]
        for si in si_obj.browse(cr, uid, inventory_ids, context=context):
            for sm in si.move_ids:
                if sm.location_id.usage == 'internal':
                    # This a loss
                    qty = - sm.product_qty
                else:
                    # This a gain
                    qty = sm.product_qty
                # TODO FIXME : manage UoM 'product_uom'
                pp_res[sm.product_id.id]['qty_variation'] += qty

        wizard_valuation = 0
        for k, v in pp_res.items():
            pp = pp_obj.browse(cr, uid, k, context=context)
            current_valuation = pp.standard_price *\
                (v['qty_available'] + v['qty_variation'])
            wizard_valuation += current_valuation
            current_pc_line = False
            for pc_line in sevw.category_line_ids:
                if pp.categ_id.id == pc_line.category_id.id:
                    current_pc_line = pc_line
                    break
            pc_res[pc_line.category_id.id]['valuation'] += current_valuation

            # Create a Product Line
            sevwpl_obj.create(cr, uid, {
                'category_line_id': current_pc_line.id,
                'product_id': k,
                'qty_available': v['qty_available'],
                'qty_variation': v['qty_variation'],
                'qty_total': v['qty_available'] + v['qty_variation'],
                'valuation': current_valuation,
            }, context=context)

        # Update Category Lines Valuation
        for pc_line in sevw.category_line_ids:
            sevwcl_obj.write(cr, uid, [pc_line.id], {
                'valuation': pc_res[pc_line.category_id.id]['valuation'],
            }, context=context)

        # Update Wizard Valuation
        self.write(cr, uid, [id], {
            'state': 'done',
            'total_valuation': wizard_valuation,
            }, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.easy.valuation.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    # Columns Section
    _columns = {
        'state': fields.selection([
            ('draft', 'Draft Wizard'),
            ('done', 'Compute Done')],
            'State', required=True, readonly=True),
        'valuation_date': fields.datetime(
            'Valuation Date', required=True),
        'print_date': fields.datetime(
            'Print Date', required=True),
        'category_line_ids': fields.one2many(
            'stock.easy.valuation.wizard.category.line', 'wizard_id',
            'Category', readonly=True),
        'inventory_ids': fields.many2many(
            'stock.inventory', 'stock_easy_valuation_inventory_rel',
            'wizard_id', 'iventory_id', 'Inventories'),
        'total_valuation': fields.float(
            'Total Valuation', readonly=True),
        'company_id': fields.many2one(
            'res.company', 'Company', select=True),
    }

    # Default values Section
    _defaults = {
        'state': 'draft',
        'print_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'company_id': lambda self, cr, uid, c: (
            self.pool.get('res.users').browse(cr, uid, uid, c).company_id.id),
    }
