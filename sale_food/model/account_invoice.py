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
from openerp.tools.translate import _


class account_invoice_line(Model):
    _inherit = 'account.invoice.line'

    # Fields Function section
    def _get_extra_food_info(self, cr, uid, ids, name, arg, context=None):
        """Return extra information about food for invoices"""
        res = {}
        if context is None:
            context = {}
        for ail in self.browse(cr, uid, ids, context=context):
            res[ail.id] = ""
            product = ail.product_id
            if product:
                if product.country_id:
                    res[ail.id] += _(' - Country: ')\
                        + product.country_id.name
                if product.fresh_category:
                    res[ail.id] += _(" - Category: ") + product.fresh_category
                label = False
                for label in product.label_ids:
                    if label.mandatory_on_invoice:
                        if label:
                            label = True
                            res[ail.id] += _(" - Label: ")
                        res[ail.id] += label.name
        return res

    # Columns Section
    _columns = {
        'extra_food_info': fields.function(
            _get_extra_food_info, type='char',
            string='Extra information for invoices'),
        }
