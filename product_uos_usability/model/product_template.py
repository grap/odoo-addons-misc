# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - UoS usability module for Odoo
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
from openerp.osv.osv import except_osv
from openerp.tools.translate import _
from openerp.addons import decimal_precision as dp


class product_template(Model):
    _inherit = 'product.template'


    # Columns Section
    _columns = {
        'uos_coeff_inv': fields.float(
            string='UOS Coeff -> Unit of Measure',
            digits_compute= dp.get_precision('Product UoS'),
            help="Coefficient to convert Unit of Sale to default Unit of"
            " Mesure.\n uom = uos * coeff",
        ),
    }

    _defaults = {
        'uos_coeff_inv': 1,
    }
