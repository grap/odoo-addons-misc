# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
#    Copyright (C) 2014 - Today GRAP (http://www.grap.coop)
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


class ProductDeliveryCategory(Model):
    _name = 'product.delivery.category'
    _order = 'sequence, name'

    # Column Section
    _columns = {
        'name': fields.char(
            'Name', required=True),
        'sequence': fields.integer(
            'Sequence', required=True),
        'image': fields.binary(
            'Image'),
        'company_id': fields.many2one(
            'res.company', string='Company', required=True),
        'active': fields.boolean('Active'),
        'sale_delay': fields.integer('Days required before delivery'),
        'product_ids': fields.one2many(
            'product.product', 'delivery_categ_id', 'Products'),
    }

    _defaults = {
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
        'active': True,
        'sale_delay': 0,
    }

    def write(self, cr, uid, ids, vals, context=None):
        "Apply sale_delay value to linked products"
        pp_obj = self.pool['product.product']
        res = super(ProductDeliveryCategory, self).write(
            cr, uid, ids, vals, context=context)
        if vals.get('sale_delay', False):
            for categ in self.browse(cr, uid, ids, context=context):
                pp_ids = [x.id for x in categ.product_ids]
                pp_obj.write(cr, uid, pp_ids, {
                    'sale_delay': categ.sale_delay,
                }, context=context)
        return res
