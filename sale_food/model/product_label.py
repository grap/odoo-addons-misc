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


class product_label(Model):
    _name = 'product.label'

    # Columns Section
    _columns = {
        'code': fields.char(
            'Code', required=True, size=32),
        'name': fields.char(
            'Name', required=True, size=64),
        'image': fields.binary('Image'),
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
