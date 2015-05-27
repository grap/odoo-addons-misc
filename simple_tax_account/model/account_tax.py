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
from openerp.osv.osv import except_osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


class AccountTax(Model):
    _inherit = 'account.tax'

    _columns = {
        'simple_tax_id': fields.many2one(
            'account.tax', string='Related Tax', help="""If the current"""
            """ tax is flagged as included, set here a tax flagged as"""
            """ excluded. Otherwise, set a tax flagged as included."""
        ),
    }

    # Custom Section
    def _translate_simple_tax(
            self, cr, uid, partner_id, price_unit, tax_ids, context=None):
        rp_obj = self.pool['res.partner']
        res = {
            'price_unit': price_unit,
            'tax_ids': tax_ids,
        }
        if not partner_id or len(tax_ids) == 0 or not price_unit:
            return res
        rp = rp_obj.browse(cr, uid, partner_id, context=context)
        if rp.simple_tax_type == 'none':
            # Tax Changes is not required
            return res
        at_lst = self.browse(cr, uid, tax_ids, context=context)
        is_percent = all([at.type == 'percent' for at in at_lst])
        is_same_type = all([
            at.price_include == at_lst[0].price_include for at in at_lst])

        if not (is_percent and is_same_type):
            # Tax changes is not possible
            # Developer Note: This algorithm could be improved to manage this
            # case.
            return res
        if ((not at_lst[0].price_include
                and rp.simple_tax_type == 'excluded') or
            (at_lst[0].price_include
                and rp.simple_tax_type == 'included')):
            # Tax changes is not required
            return res
        new_tax_ids = []
        for at in at_lst:
            if not at.simple_tax_id:
                raise except_osv(
                    _('Missing Configuration!'),
                    _("""Please ask to your accountant to set a Related"""
                        """ Tax for the tax %s.""") % (at.name))
            if at.price_include:
                price_unit = price_unit / (1 + at.amount)
            else:
                price_unit = price_unit * (1 + at.amount)
            new_tax_ids.append(at.simple_tax_id.id)
        return {
            'price_unit': price_unit,
            'tax_ids': new_tax_ids,
        }

    # Constraints Section
    def _check_simple_tax_id(self, cr, uid, ids, context=None):
        for at in self.browse(cr, uid, ids, context=context):
            if at.simple_tax_id:
                if at.price_include == at.simple_tax_id.price_include:
                    return False
        return True

    _constraints = [
        (
            _check_simple_tax_id,
            """Error: The current Tax and the Related Tax have the"""
            """ same settings for the field 'Tax Included in Price'""",
            ['price_include', 'simple_tax_id']),
    ]
