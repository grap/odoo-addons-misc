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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class product_pricetag_wizard_line(TransientModel):
    _name = 'product.pricetag.wizard.line'
    _rec_name = 'product_id'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'product.pricetag.wizard', 'Wizard', select=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True),
        'quantity': fields.integer(
            'Quantity', required=True),
        'print_unit_price': fields.boolean(
            'Print unit price'),
    }

    # Defaults Section
    _defaults = {
        'quantity': 1,
        'print_unit_price': True,
    }
