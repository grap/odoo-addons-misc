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

import math

from openerp.osv.orm import Model
from openerp.tools.translate import _


class SaleOrderLine(Model):
    _inherit = 'sale.order.line'

    def _eshop_round_value(self, product, qty):
        if product.eshop_unpack_qty and qty < product.eshop_minimum_qty:
            rounded_qty = product.eshop_unpack_qty
        else:
            rounded_qty = product.eshop_rounded_qty
        digit = len(str(float(rounded_qty) - int(rounded_qty)).split('.')[1])
        division = float(qty) / rounded_qty
        if division % 1 == 0:
            return qty
        else:
            return round(math.ceil(division) * rounded_qty, digit)

    def product_id_change(
            self, cr, uid, ids, pricelist, product_id, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None):
        """
        Manage minimum / rounded and unpacking quantity. (with surcharge)
        return 'info' value instead of 'warning' value to avoid blocking
        message for end users.
        """
        is_eshop = self.pool['res.users'].has_group(
            cr, uid, 'sale_eshop.res_groups_is_eshop')
        infos = []
        computed_discount = False
        product = self.pool['product.product'].browse(
            cr, uid, product_id, context=context)
        if qty and is_eshop and product_id:
            computed_discount = True
            discount = 0
            if product.eshop_minimum_qty:
                rounded_qty = self._eshop_round_value(product, qty)
                if qty < product.eshop_minimum_qty:
                    if product.eshop_unpack_qty:
                        if rounded_qty < product.eshop_minimum_qty:
                            # rounding qty didn't make it reach the minimum qty
                            infos.append(_(
                                " The quantity '%.3f' for the product '%s' is"
                                " under the minimum quantity '%.3f'. A %d%%"
                                " surcharge has been applied.") % (
                                qty, product.name,
                                product.eshop_minimum_qty,
                                product.eshop_unpack_surcharge))
                            discount = - product.eshop_unpack_surcharge
                        else:
                            infos.append(_(
                                "'%.3f' is not a valid quantity for %s, the"
                                " minimum quantity is '%.3f'. The quantity"
                                "  has been automatically increased in your"
                                " shopping cart.") % (
                                qty, product.name,
                                product.eshop_minimum_qty))
                        if qty != rounded_qty:
                            # The quantity has been rounded
                            infos.append(_(
                                "'%.3f' is not a valid quantity for %s, the"
                                " quantity has been rounded to '%.3f'.") % (
                                qty, product.name, rounded_qty))
                            qty = rounded_qty
                    else:
                        infos.append(_(
                            "'%.3f' is not a valid quantity for %s, the "
                            " minimum quantity is %'%.3f'. The quantity has"
                            " been automatically increased in your shopping"
                            " cart.") % (
                            qty, product.name, product.eshop_minimum_qty))
                        qty = product.eshop_minimum_qty
                else:
                    if qty != rounded_qty:
                        # The quantity has been rounded
                        infos.append(_(
                            "'%.3f' is not a valid quantity for %s, the"
                            " quantity has been rounded to '%.3f'.") % (
                            qty, product.name, rounded_qty))
                        qty = rounded_qty

        res = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product_id, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order,
            packaging=packaging, fiscal_position=fiscal_position,
            flag=flag, context=context)
        res['infos'] = infos
        res['value']['product_uom_qty'] =\
            res['value'].get('product_uom_qty', qty)
        if computed_discount:
            res['value']['discount'] = discount
        return res
