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


class product_product(Model):
    _inherit = 'product.product'


    def onchange_uos_coeff_inv(
            self, cr, uid, ids, uos_coeff_inv, context=None):
        if not uos_coeff_inv:
            raise except_osv(_('Error!'), _(
                "The fields 'UoS Coeff' can not be null."))
        else:
            res = {'value': {
                'uos_coeff':  1 / float(uos_coeff_inv),
            }}
        return res
