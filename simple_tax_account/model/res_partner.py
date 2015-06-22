# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Simple Tax module for Odoo
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


SIMPLE_TAX_TYPE_KEYS = [
    ('none', 'Undefined'),
    ('excluded', 'Exclude Tax in Prices'),
    ('included', 'Include Tax in Prices'),
]


class ResPartner(Model):
    _inherit = 'res.partner'

    _columns = {
        'simple_tax_type': fields.selection(
            SIMPLE_TAX_TYPE_KEYS, 'Tax Type', required=True),
    }

    _defaults = {
        'simple_tax_type': 'none',
    }
