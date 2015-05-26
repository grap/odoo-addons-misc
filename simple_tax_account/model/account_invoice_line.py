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

from openerp.osv.orm import Model


class AccountInvoiceLine(Model):
    _inherit = 'account.invoice.line'

    def product_id_change(
            self, cr, uid, ids, product, uom_id, qty=0, name='',
            type='out_invoice', partner_id=False, fposition_id=False,
            price_unit=False, currency_id=False, context=None,
            company_id=None):
        at_obj = self.pool['account.tax']
        res = super(AccountInvoiceLine, self).product_id_change(
            cr, uid, ids, product, uom_id, qty=qty, name=name,
            type=type, partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id, context=context,
            company_id=company_id)

        if res['value'].get('price_unit', False):
            info = at_obj._translate_simple_tax(
                cr, uid, partner_id, res['value']['price_unit'],
                res['value']['invoice_line_tax_id'], context=context)
            res['value'].update({
                'price_unit': info['price_unit'],
                'invoice_line_tax_id': info['tax_ids'],
            })
        return res
