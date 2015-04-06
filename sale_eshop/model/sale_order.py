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


from openerp.osv.orm import Model


class SaleOrder(Model):
    _inherit = 'sale.order'

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
                'image_small': ec.image_small,
                'product_ids': [],
            }
            for pp in ec.available_product_ids:
                current_categ['product_ids'].append({
                    'id': pp.id,
                    'name': pp.name,
                    'image_small': pp.image_small,
                    'list_price': pp.list_price,
                    'uom_eshop_description': pp.uom_id.eshop_description,
                    'current_qty': qty_dict.get(pp.id, 0)
                })
            res.append(current_categ)
        return res
