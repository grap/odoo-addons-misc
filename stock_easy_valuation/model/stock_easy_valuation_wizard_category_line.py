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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class stock_easy_valuation_wizard_category_line(TransientModel):
    _name = 'stock.easy.valuation.wizard.category.line'
    _rec_name = 'category_id'

    def _get_total(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for sevwcl in self.browse(cr, uid, ids, context):
            # compute products valuation and quantity in the current category
            total_valuation = sevwcl.valuation
            total_product_qty = len(sevwcl.product_line_ids)

            # Get category child of the current category
            child_pc_ids = [x.id for x in sevwcl.category_id.child_id]

            # Compute the valuation of each child
            child_sevwcl_ids = self.search(cr, uid, [
                ('wizard_id', '=', sevwcl.wizard_id.id),
                ('category_id', 'in', child_pc_ids),
            ], context=context)
            for child_sevwcl in self.browse(
                    cr, uid, child_sevwcl_ids, context=context):
                total_valuation += child_sevwcl.total_valuation
                total_product_qty += child_sevwcl.total_product_qty
            res[sevwcl.id] = {
                'total_valuation': total_valuation,
                'total_product_qty': total_product_qty,
            }
        return res

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'stock.easy.valuation.wizard',
            'Wizard', select=True),
        'category_id': fields.many2one(
            'product.category', 'Category', readonly=True),
        'product_line_ids': fields.one2many(
            'stock.easy.valuation.wizard.product.line', 'category_line_id',
            'Products', readonly=True),
        'valuation': fields.float(
            'Valuation', readonly=True),
        'total_valuation': fields.function(
            _get_total, type='float', multi="_get_total",
            string='Total Valuation'),
        'total_product_qty': fields.function(
            _get_total, type='integer', multi="_get_total",
            string='Total Product Quantity'),
    }
