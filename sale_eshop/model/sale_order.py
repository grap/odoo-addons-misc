# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - eShop for Odoo
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

from datetime import datetime

from openerp.tools.translate import _
from openerp.osv.orm import Model


class SaleOrder(Model):
    _inherit = 'sale.order'

    # Custom Section for eshop
    def eshop_get_current_sale_order_id(
            self, cr, uid, partner_id, context=None):
        order_ids = self.search(cr, uid, [
            ('partner_id', '=', partner_id),
            ('user_id', '=', uid),
            ('state', '=', 'draft')], context=context)
        return order_ids and order_ids[0] or False

    def eshop_set_quantity(
            self, cr, uid, partner_id, product_id, quantity, method,
            context=None):
        line_obj = self.pool['sale.order.line']
        partner_obj = self.pool['res.partner']
        user_obj = self.pool['res.users']

        order_id = self.eshop_get_current_sale_order_id(
            cr, uid, partner_id, context=context)

        if not order_id:
            # Create Sale Order
            partner = partner_obj.browse(cr, uid, partner_id, context=context)
            if partner.property_product_pricelist:
                pricelist_id = partner.property_product_pricelist.id
            else:
                user = user_obj.browse(cr, uid, uid, context=context)
                pricelist_id = user.company_id.eshop_pricelist_id.id
            order_id = self.create(
                cr, uid, {
                    'partner_id': partner_id,
                    'partner_invoice_id': partner_id,
                    'partner_shipping_id': partner_id,
                    'pricelist_id': pricelist_id,
                }, context=context)
        order = self.browse(cr, uid, order_id, context=context)

        # Search Line
        current_line_id = False
        for line in order.order_line:
            if line.product_id.id == product_id:
                current_line_id = line.id
                if method == 'add':
                    quantity += line.product_uom_qty
                break

        if quantity != 0:
            # We set a not null quantity
            res = line_obj.product_id_change(
                cr, uid, False, order.pricelist_id.id, product_id,
                qty=quantity, partner_id=partner_id, context=context)

            line_data = {k: v for k, v in res['value'].items()}

            # F& !! ORM
            if line_data['tax_id']:
                line_data['tax_id'] = [[6, False, line_data['tax_id']]]
            else:
                line_data['tax_id'] = [[6, False, []]]

            # Create line if needed
            if not current_line_id:
                line_data['product_id'] = product_id
                line_data['order_id'] = order_id
                current_line_id = line_obj.create(
                    cr, uid, line_data, context=context)
            else:
                line_obj.write(
                    cr, uid, [current_line_id], line_data, context=context)
            line = line_obj.browse(cr, uid, current_line_id, context=context)
            res = {
                'messages': res['infos'],
                'quantity': line.product_uom_qty,
                'changed': (quantity != line.product_uom_qty),
                'price_subtotal': line.price_subtotal,
                'price_subtotal_gross': line.price_subtotal_gross,
                'discount': line.discount,
            }
        else:
            res = {
                'quantity': 0,
                'changed': False,
                'price_subtotal': 0,
                'price_subtotal_gross': 0,
                'discount': 0,
            }
            if current_line_id:
                if len(order.order_line) == 1:
                    # We unlink the whole order
                    self.unlink(cr, uid, [order_id], context=context)
                    order_id = False
                    res['messages'] = [_(
                        "The Shopping Cart has been successfully deleted.")]
                else:
                    # We unlink the line
                    line_obj.unlink(
                        cr, uid, [current_line_id], context=context)
                    res['messages'] = [_(
                        "The line has been successfully deleted")]

        # TODO Update amount on sale order if needed

        res.update(self.eshop_sale_order_info(
            cr, uid, order_id, context=context))
        return res

    def eshop_sale_order_info(self, cr, uid, order_id, context=None):
        if order_id:
            order = self.browse(cr, uid, order_id, context=context)
            return {
                'amount_untaxed': order.amount_untaxed,
                'amount_tax': order.amount_tax,
                'amount_total': order.amount_total,
                'order_id': order_id,
            }
        else:
            return {
                'amount_untaxed': 0,
                'amount_tax': 0,
                'amount_total': 0,
                'order_id': False,
            }

    def send_mail(self, cr, uid, ids, context=None):
        context = context or {}
        imd_obj = self.pool['ir.model.data']
        et_obj = self.pool['email.template']
        et = imd_obj.get_object(
            cr, uid, 'sale', 'email_template_edi_sale')
        for so in self.browse(cr, uid, ids, context=context):
            et_obj.send_mail(cr, uid, et.id, so.id, True, context=context)
        return {}
