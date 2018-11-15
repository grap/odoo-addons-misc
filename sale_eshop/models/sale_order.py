# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # API Section
    @api.model
    def eshop_get_current_sale_order_id(self, partner_id):
        order_ids = self.search([
            ('partner_id', '=', partner_id),
            ('user_id', '=', self.env.user.id),
            ('state', '=', 'draft')])
        return order_ids and order_ids[0].id or False

    @api.model
    def eshop_set_quantity(
            self, partner_id, product_id, quantity, method):
        """@method : 'set' / 'add'"""
        SaleOrderLine = self.env['sale.order.line']
        ResPartner = self.env['res.partner']

        order_id = self.eshop_get_current_sale_order_id(partner_id)

        if not order_id:
            # Create Sale Order
            partner = ResPartner.browse(partner_id)
            if partner.property_product_pricelist:
                pricelist_id = partner.property_product_pricelist.id
            else:
                pricelist_id = self.env.user.company_id.eshop_pricelist_id.id
            order = self.create({
                'partner_id': partner_id,
                'partner_invoice_id': partner_id,
                'partner_shipping_id': partner_id,
                'pricelist_id': pricelist_id,
            })
        else:
            order = self.browse(order_id)

        # Search Line
        current_line = False
        for line in order.order_line:
            if line.product_id.id == product_id:
                current_line = line
                if method == 'add':
                    quantity += line.product_uom_qty
                break

        if quantity != 0:
            # We set a not null quantity
            res = SaleOrderLine.product_id_change(
                order.pricelist_id.id, product_id,
                qty=quantity, partner_id=partner_id)

            line_vals = {k: v for k, v in res['value'].items()}

            # F& !! ORM
            if line_vals['tax_id']:
                line_vals['tax_id'] = [[6, False, line_vals['tax_id']]]
            else:
                line_vals['tax_id'] = [[6, False, []]]

            # Create line if needed
            if not current_line:
                line_vals['product_id'] = product_id
                line_vals['order_id'] = order.id
                current_line = SaleOrderLine.create(line_vals)
            else:
                current_line.write(line_vals)
            res = {
                'messages': res['infos'],
                'quantity': current_line.product_uom_qty,
                'changed': (quantity != current_line.product_uom_qty),
                'price_subtotal': current_line.price_subtotal,
                'price_subtotal_gross': current_line.price_subtotal_gross,
                'discount': current_line.discount,
            }
        else:
            res = {
                'quantity': 0,
                'changed': False,
                'price_subtotal': 0,
                'price_subtotal_gross': 0,
                'discount': 0,
            }
            if current_line:
                if len(order.order_line) == 1:
                    # We unlink the whole order
                    order.unlink()
                    order_id = False
                    res['messages'] = [_(
                        "The Shopping Cart has been successfully deleted.")]
                else:
                    # We unlink the line
                    current_line.unlink()
                    res['messages'] = [_(
                        "The line has been successfully deleted")]

        res.update(self._eshop_sale_order_info(order))
        return res

    @api.multi
    def eshop_set_as_sent(self):
        self.signal_workflow('quotation_sent')

    @api.model
    def _eshop_cron_confirm_orders(self):
        eshop_group = self.env.ref('sale_eshop.res_groups_is_eshop')
        eshop_users = eshop_group.users
        for user in eshop_users:
            local_self = self.sudo(user)
            orders = local_self.search([
                ('state', '=', 'sent'),
                ('user_id', '=', user.id),
            ])
            for order in orders:
                order.with_context(send_email=True).action_button_confirm()

    # Custom Section
    def _eshop_sale_order_info(self, order):
        if order:
            return {
                'amount_untaxed': order.amount_untaxed,
                'amount_tax': order.amount_tax,
                'amount_total': order.amount_total,
                'order_id': order.id,
            }
        else:
            return {
                'amount_untaxed': 0,
                'amount_tax': 0,
                'amount_total': 0,
                'order_id': False,
            }
