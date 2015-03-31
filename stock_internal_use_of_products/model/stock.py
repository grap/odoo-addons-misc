# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Internal Use Of Products for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv.orm import Model


class stock_move(Model):
    _inherit = "stock.move"

    def _get_reference_accounting_values_for_valuation(
            self, cr, uid, move, context=None):
        tax_obj = self.pool.get('account.tax')
        obj_product = move.product_id
        reference_amount, reference_currency_id = super(
            stock_move, self)._get_reference_accounting_values_for_valuation(
            cr, uid, move, context=context)
        reference_amount = move.product_qty * tax_obj.compute_all(
            cr, uid, obj_product.supplier_taxes_id,
            obj_product.standard_price, 1, obj_product.id, False)['total']
        return reference_amount, reference_currency_id
