# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Simple Tax module for Odoo
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
from .res_partner import SIMPLE_TAX_TYPE_KEYS


class AccountInvoice(Model):
    _inherit = 'account.invoice'

    _columns = {
        'simple_tax_type': fields.related(
            'partner_id', 'simple_tax_type', type='selection',
            selection=SIMPLE_TAX_TYPE_KEYS, string='Tax Type',
            readonly='True'),
    }

    def recompute_simple_tax(self, cr, uid, ids, context=None):
        at_obj = self.pool['account.tax']
        ail_obj = self.pool['account.invoice.line']

        for ai in self.browse(cr, uid, ids, context=context):
            for ail in ai.invoice_line:
                info = at_obj._translate_simple_tax(
                    cr, uid, ai.partner_id.id, ail.price_unit,
                    [x.id for x in ail.invoice_line_tax_id], context=context)
                if (set(info['tax_ids']) !=
                        set([x.id for x in ail.invoice_line_tax_id])
                        or ail.price_unit != info['price_unit']):
                    ail_obj.write(cr, uid, [ail.id], {
                        'price_unit': info['price_unit'],
                        'invoice_line_tax_id': [(6, 0, info['tax_ids'])],
                    }, context=context)
        return True
