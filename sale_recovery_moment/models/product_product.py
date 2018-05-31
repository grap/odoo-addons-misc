# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
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


from openerp.osv import fields
from openerp.osv.orm import Model


class ProductProduct(Model):
    _inherit = 'product.product'

    # Column Section
    _columns = {
        'prepare_categ_id': fields.many2one(
            'product.prepare.category', 'Prepare Category'),

        'delivery_categ_id': fields.many2one(
            'product.delivery.category', 'Delivery Category'),
    }

    # Custom Section
    def get_sale_delay_from_delivery_categ(
            self, cr, uid, vals, context=None):
        pdc_obj = self.pool['product.delivery.category']
        if vals.get('delivery_categ_id', False):
            pdc = pdc_obj.browse(
                cr, uid, vals['delivery_categ_id'], context=context)
            vals['sale_delay'] = pdc.sale_delay
        return vals

    def create(self, cr, uid, vals, context=None):
        # TODO FIXME.
        # In GRAP Instance, one function (copy or copy_data) is bad
        # designed. (api.multi? api.one?) So the vals is not a dict but
        # a list of one dict.
        if type(vals) is list:
            vals = vals[0]
        vals = self.get_sale_delay_from_delivery_categ(
            cr, uid, vals, context=context)
        return super(ProductProduct, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        vals = self.get_sale_delay_from_delivery_categ(
            cr, uid, vals, context=context)
        return super(ProductProduct, self).write(
            cr, uid, ids, vals, context=context)
