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

import hashlib
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

    def get_current_eshop_product_list(self, cr, uid, id, context=None):
        """The aim of this function is to deal with delay of response of
        the odoo-eshop, module.
        This will return a dictionnary of eshop.category, with all products
        information"""
        res = []
        ec_obj = self.pool['eshop.category']
        pp_obj = self.pool['product.product']
        label_obj = self.pool['product.label']
        qty_dict = {}
        # Get current quantities ordered
        if id:
            so = self.browse(cr, uid, id, context=context)
            for sol in so.order_line:
                if sol.product_id.id in qty_dict.keys():
                    qty_dict[sol.product_id.id] += sol.product_uom_qty
                else:
                    qty_dict[sol.product_id.id] = sol.product_uom_qty

        # Return product and categories
        ec_ids = ec_obj.search(
            cr, uid, [('type', '=', 'normal')], context=context)
        for ec in ec_obj.browse(cr, uid, ec_ids):
            if ec.available_product_qty == 0:
                continue
            current_categ = {
                'id': ec.id,
                'name': ec.name,
                'complete_name': ec.complete_name,
                'sha1': hashlib.sha1(str(ec_obj.perm_read(
                    cr, uid, [ec.id])[0]['write_date'])).hexdigest(),
                'product_ids': [],
            }
            for product in ec.available_product_ids:
                current_product = {
                    'id': product.id,
                    'name': product.name,
                    'default_code': product.default_code,
                    'list_price': product.list_price,
                    'uom_eshop_description': product.uom_id.eshop_description,
                    'eshop_taxes_description': product.eshop_taxes_description,
                    'current_qty': qty_dict.get(product.id, 0),
                    'label_ids': [],
                    'sha1': hashlib.sha1(str(pp_obj.perm_read(
                        cr, uid, [product.id])[0]['write_date'])).hexdigest(),
                }
                if product.delivery_categ_id:
                    current_product['delivery_categ_id'] = {
                        'id': product.delivery_categ_id.id,
                        'name': product.delivery_categ_id.name,
                    }
                for label in product.label_ids:
                    current_product['label_ids'].append({
                        'id': label.id,
                        'name': label.name,
                        'sha1': hashlib.sha1(str(label_obj.perm_read(
                            cr, uid,
                            [label.id])[0]['write_date'])).hexdigest(),
                    })
                current_categ['product_ids'].append(current_product)
            res.append(current_categ)
        return res
