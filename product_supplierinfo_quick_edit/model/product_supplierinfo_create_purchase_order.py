# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Supplier Info Quick Edit module for Odoo
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

from openerp.tools.translate import _
from openerp.osv.orm import TransientModel


class product_supplierinfo_create_purchase_order(TransientModel):
    _name = 'product.supplierinfo.create.purchase.order'

    def _get_product_from_template(
            self, cr, uid, template_ids, context=None):
        """
        Return product.product ids according to the template_ids given.
        By default, return all the products linked to the templates.
        Note 1:
        This function exists mainly to be easily overloaded.
        Note 2:
        This function exists because Odoo set a dummy link between template
        and supplierinfo, that is rather moronic. (should be product.product).
        Maybe in Odoo V43, this will be fixed, making this function useless.
        """
        product_obj = self.pool['product.product']
        return product_obj.search(
            cr, uid, [('product_tmpl_id', 'in', template_ids)],
            context=context)

    def create_purchase_order(self, cr, uid, ids, context=None):
        supplierinfo_ids = context.get('active_ids', [])
        user_obj = self.pool['res.users']
        value_obj = self.pool['ir.values']
        supplierinfo_obj = self.pool['product.supplierinfo']
        order_obj = self.pool['purchase.order']
        line_obj = self.pool['purchase.order.line']

        create_data = {}
        order_ids = []

        # Get supplier and products
        for supplierinfo in supplierinfo_obj.browse(
                cr, uid, supplierinfo_ids, context=context):
            product_ids = self._get_product_from_template(
                cr, uid, [supplierinfo.product_id.id], context=context)
            if supplierinfo.name.id in create_data:
                create_data[supplierinfo.name.id] += product_ids
            else:
                create_data[supplierinfo.name.id] = product_ids

        # Create Purchase Orders
        for partner_id, product_ids in create_data.iteritems():
            order_data = order_obj._add_missing_default_values(
                cr, uid, {}, context=context)
            order_data['partner_id'] = partner_id
            order_data.update(order_obj.onchange_partner_id(
                cr, uid, False, partner_id)['value'])

            # Get default warehouse
            warehouse_id = value_obj.get_default(
                cr, uid, 'purchase.order', 'warehouse_id',
                company_id=user_obj._get_company(cr, uid))

            # Get default stock location
            order_data['location_id'] = order_obj.onchange_warehouse_id(
                cr, uid, [], warehouse_id)['value']['location_id']

            order_id = order_obj.create(cr, uid, order_data, context=context)

            for product_id in product_ids:
                line_data = {
                    'order_id': order_id,
                    'product_id': product_id,
                }
                line_data.update(line_obj.onchange_product_id(
                    cr, uid, ids, order_data['pricelist_id'], product_id, 0,
                    False, order_data['partner_id'], context=context)['value'])

                line_obj.create(cr, uid, line_data, context=context)

            order_ids.append(str(order_id))

        return {
            'domain': "[('id','in', [" + ','.join(order_ids) + "])]",
            'name': _('Purchase Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
