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


class res_company(Model):
    _inherit = 'res.company'

    _columns = {
        'pricetag_image': fields.binary(
            'Price Tag Image',
            help="""This field will be printed on Price Tag."""
            """Size : 210px * 210px"""),
        'pricetag_color': fields.char(
            'Price Tag Color', required=True, size=7,
            help="Color of the Price Tag by default. Format #RRGGBB"),
        'certifier_organization_id': fields.many2one(
            'certifier.organization', 'Certifier Organization'),
    }

    _defaults = {
        'pricetag_color': '#FFFFFF',
    }

    # Demo Function Section
    def _demo_init_image(self, cr, uid, ids=None, context=None):
        demo_image.init_image(
            self.pool, cr, uid, 'res.company', 'pricetag_image',
            '/../static/src/img/demo/res_company/', context=context)
