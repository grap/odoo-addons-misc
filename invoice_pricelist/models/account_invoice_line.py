# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # View Section
    @api.multi
    def product_id_change(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None):
        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)
        res['value'].pop('price_unit', False)
        return res

    @api.multi
    def onchange_product_id_pricelist(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None, pricelist_id=False):
        sale_order_line_obj = self.env['sale.order.line']
        purchase_order_line_obj = self.env['purchase.order.line']

        # Call regular Super
        res = self.product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)
        if type in ('out_invoice', 'out_refund'):
            # Customer part
            sale_res = sale_order_line_obj.product_id_change(
                pricelist_id, product, qty=qty,
                uom=uom_id, qty_uos=qty, uos=uom_id, name=name,
                partner_id=partner_id, lang=False, update_tax=True,
                date_order=False, packaging=False,
                fiscal_position=fposition_id, flag=False)
            print sale_res
            if 'price_unit' in sale_res['value']:
                res['value']['price_unit'] = sale_res['value']['price_unit']

        elif type in ('in_invoice', 'in_refund'):
            # Supplier part
            purchase_res = purchase_order_line_obj.onchange_product_id(
                pricelist_id, product, qty, uom_id,
                partner_id, date_order=False, fiscal_position_id=fposition_id,
                date_planned=False, name=name, price_unit=False)
            if 'price_unit' in purchase_res['value']:
                res['value']['price_unit'] =\
                    purchase_res['value']['price_unit']

        return res
