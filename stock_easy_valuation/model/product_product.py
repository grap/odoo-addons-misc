# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Easy Valuation for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

from openerp.osv import fields
from openerp.osv.orm import Model


class product_product(Model):
    _inherit = 'product.product'

    def _get_valuation_qty_available(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            res[pp.id] = pp.qty_available * pp.standard_price
        return res

    def _get_valuation_virtual_available(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            res[pp.id] = pp.virtual_available * pp.standard_price
        return res

    _columns = {
        'valuation_qty_available': fields.function(
            _get_valuation_qty_available, type='float',
            string='Valuation of Quantity on Hand'),
        'valuation_virtual_available': fields.function(
            _get_valuation_virtual_available, type='float',
            string='Valuation of Virtual Quantity'),
    }
