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

from openerp.osv.orm import Model


class SaleOrder(Model):
    _inherit = 'sale.order'

    # Custom Section
    def select_delivery_moment_id(
            self, cr, uid, id, delivery_moment_id, context=None):
        sdm_obj = self.pool['sale.delivery.moment']
        sol_obj = self.pool['sale.order.line']
        so = self.browse(cr, uid, id, context=context)
        now = datetime.now()

        delivery_moments_data = sdm_obj.load_delivery_moment_data(
            cr, uid, so.id, so.company_id.eshop_minimum_price,
            so.company_id.eshop_vat_included, context=context)

        delivery_moment_data = False
        for item in delivery_moments_data:
            if item['id'] == delivery_moment_id:
                delivery_moment_data = item

        if not delivery_moment_data:
            return False
        if not (delivery_moment_data['is_delay_possible']
                and delivery_moment_data['is_limit_ok']):
            return False
        if delivery_moment_data['is_partial']:
            # Create a New Draft Order and move some lines
            moment = sdm_obj.browse(
                cr, uid, delivery_moment_id, context=context)
            draft_order_id = self.copy(cr, uid, so.id, context=context)
            line_to_move_ids = []
            for line in so.order_line:
                if not sdm_obj.check_possibility(
                        cr, uid, line, moment, now, context=None):
                    line_to_move_ids.append(line.id)

            # Remove lines from Copied Sale Order
            draft_order = self.browse(
                cr, uid, draft_order_id, context=context)
            sol_obj.unlink(
                cr, uid, [x.id for x in draft_order.order_line],
                context=context)
            # Move line from original sale order to new Sale Order
            sol_obj.write(
                cr, uid, line_to_move_ids, {'order_id': draft_order_id},
                context=context)

        # Fix Odoo Bug change line doesn't recompute amount_all
        original_order = self.browse(cr, uid, id, context=context)
        sol_obj.write(
            cr, uid, [original_order.order_line[0].id],
            {'price_unit': original_order.order_line[0].price_unit},
            context=context)
        if delivery_moment_data['is_partial']:
            draft_order = self.browse(cr, uid, draft_order_id, context=context)
            sol_obj.write(
                cr, uid, [draft_order.order_line[0].id],
                {'price_unit': draft_order.order_line[0].price_unit},
                context=context)

        # Validate the order
        self.write(
            cr, uid, [id], {'delivery_moment_id': delivery_moment_id},
            context=context)
        self.action_button_confirm(cr, uid, [id], context=context)
        self.send_mail(cr, uid, [id], context=context)
        return True

    def send_mail(self, cr, uid, ids, context=None):
        context = context or {}
        imd_obj = self.pool['ir.model.data']
        et_obj = self.pool['email.template']
        et = imd_obj.get_object(
            cr, uid, 'sale', 'email_template_edi_sale')
        for so in self.browse(cr, uid, ids, context=context):
            et_obj.send_mail(cr, uid, et.id, so.id, True, context=context)
        return {}
