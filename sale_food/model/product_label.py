# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Food Module for Odoo
#    Copyright (C) 2012-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.addons.sale_food import demo_image
from openerp import tools


class product_label(Model):
    _name = 'product.label'

    # Compute Section
    def _get_image(self, cr, uid, ids, name, args, context=None):
        res = {}
        for label in self.browse(cr, uid, ids, context=context):
            res[label.id] = tools.image_get_resized_images(
                label.image, avoid_resize_medium=True)
        return res

    def _set_image(self, cr, uid, pId, name, value, args, context=None):
        return self.write(
            cr, uid, [pId], {'image': tools.image_resize_image_big(value)},
            context=context)

    # Columns Section
    _columns = {
        'code': fields.char(
            'Code', required=True, size=32),
        'name': fields.char(
            'Name', required=True, size=64),
        'image': fields.binary('Image'),
        'image_small': fields.function(
            _get_image, fnct_inv=_set_image,
            string='Small-sized image', type='binary', multi='_get_image',
            store={
                'product.label': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10)}),
        'image_medium': fields.function(
            _get_image, fnct_inv=_set_image,
            string='Medium-sized image', type='binary', multi='_get_image',
            store={
                'product.label': (
                    lambda self, cr, uid, ids, c={}: ids, ['image'], 10)}),
        'active': fields.boolean(
            'Active',
            help="""By unchecking the active field you can disable a label"""
            """ without deleting it."""),
        'mandatory_on_invoice': fields.boolean(
            'Mandatory on invoice',
            help="""By checking this field, the label will be printed on"""
            """ all the customers invoices."""),
        'minimum_social_notation': fields.integer(
            'Minimum Social Notation'),
        'minimum_local_notation': fields.integer(
            'Minimum Local Notation'),
        'minimum_organic_notation': fields.integer(
            'Minimum Organic Notation'),
        'minimum_packaging_notation': fields.integer(
            'Minimum Packaging Notation'),
        'is_organic': fields.boolean(
            'Is Organic',
            help="""Check this box if this label is an organic label."""
            """ If products has no organic label, a text will be displayed"""
            """ on Price Tag."""),
    }

    _defaults = {
        'active': True,
        'mandatory_on_invoice': False,
    }

    # Demo Function Section
    def _demo_init_image(self, cr, uid, ids=None, context=None):
        demo_image.init_image(
            self.pool, cr, uid, 'product.label', 'image',
            '/static/src/img/demo/product_label/', context=context)
