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
from openerp.osv import fields
import openerp.addons.decimal_precision as dp


class InternalUseLine(Model):
    _name = 'internal.use.line'
    _order = 'create_date'

    # Columns section
    def _get_subtotal(self, cr, uid, ids, name, args, context=None):
        res = {}
        for iul in self.pool.get('internal.use.line').browse(
                cr, uid, ids, context=context):
            res[iul.id] = iul.product_qty * iul.price_unit
        return res

    _columns = {
        'name': fields.related(
            'internal_use', 'name', string='Name', select=1),
        'company_id': fields.related(
            'internal_use', 'company_id', select=1,
            type='many2one', relation='res.company', string='Company',
            readonly=True, store=True),
        'internal_use': fields.many2one(
            'internal.use', 'Internal Uses', select=1, ondelete='cascade'),
        'internal_use_case': fields.related(
            'internal_use', 'internal_use_case', string='Internal Use Case',
            select=1, type='many2one', relation='internal.use.case',
            readonly=True, store=True),
        'date_done': fields.related(
            'internal_use', 'date_done', string='Date',
            select=1, type='date', readonly=True, store=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True, select=1),
        'product_qty': fields.float(
            'Quantity', digits_compute=dp.get_precision('Product UoM'),
            required=True),
        'product_uom_id': fields.many2one(
            'product.uom', 'Unit of Measure', required=True),
        'state': fields.related(
            'internal_use', 'state', type='char', string='State',
            readonly=True, select=1),
        'price_unit': fields.float(
            'Unit Price Tax excluded',
            digits_compute=dp.get_precision('Product Price')),
        'subtotal': fields.function(
            _get_subtotal, type='float', string='Subtotal Tax excluded',
            digits_compute=dp.get_precision('Product Price'), store=True),
    }

    # Defaults section
    _defaults = {
        'product_uom_id': False,
        'product_qty': 1,
        'price_unit': 0.0,
    }

    # Views section
    def on_change_product_id(self, cr, uid, ids, product):
        """ Changes UoM and name if product_id changes.
        @param product: Changed product_id
        @param uom: UoM product
        @return:  Dictionary of changed values
        """
        if not product:
            value = self._defaults
        else:
            tax_obj = self.pool.get('account.tax')
            obj_product = self.pool.get('product.product').browse(
                cr, uid, product)
            uom = obj_product.uom_id.id or False
            price_unit = tax_obj.compute_all(
                cr, uid, obj_product.supplier_taxes_id,
                obj_product.standard_price, 1, product, False)['total']
            value = {'price_unit': price_unit, 'product_uom_id': uom}
        return {'value': value}
