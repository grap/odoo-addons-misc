# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

from datetime import datetime, timedelta

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class SaleDeliveryMoment(Model):
    _name = 'sale.delivery.moment'

    def load_delivery_moment_data(
            self, cr, uid, sale_order_id, minimum_price, vat_included,
            context=None):
        """Load Delivery Moments, depending of the current sale order
            Mention for each delivery moment if it's possible to select it.
        """
        so_obj = self.pool['sale.order']
        so = so_obj.browse(cr, uid, sale_order_id, context=context)
        res = []
        sale_delivery_categ_id = so.partner_id.delivery_categ_id
        now = datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        if not sale_delivery_categ_id:
            return res
        moment_ids = self.search(cr, uid, [
            ('min_delivery_date', '>', now_str),
            ('delivery_categ_id', '=', sale_delivery_categ_id.id)],
            order='min_delivery_date, id',
            context=context)
        moments = self.browse(cr, uid, moment_ids, context=context)
        for moment in moments:
            amount_vat_included = 0
            amount_vat_excluded = 0
            is_delay_possible = False
            is_partial = False
            for line in so.order_line:
                line_ok = self.check_possibility(
                    cr, uid, line, moment, now, context=context)
                is_delay_possible = is_delay_possible or line_ok
                is_partial = is_partial or not line_ok
                if line_ok:
                    amount_vat_excluded += line.price_subtotal
                    amount_vat_included += line.price_subtotal_gross
            if minimum_price:
                if vat_included:
                    is_limit_ok = (minimum_price <= amount_vat_included)
                else:
                    is_limit_ok = (minimum_price <= amount_vat_excluded)
            else:
                is_limit_ok = True
            res.append({
                'id': moment.id,
                'min_delivery_date': moment.min_delivery_date,
                'max_delivery_date': moment.max_delivery_date,
                'is_complete': moment.is_complete,
                'is_delay_possible': is_delay_possible,
                'is_partial': is_partial,
                'amount_vat_excluded': amount_vat_excluded,
                'amount_vat_included': amount_vat_included,
                'is_limit_ok': is_limit_ok,
            })
        return res

    def check_possibility(
            self, cr, uid, sale_order_line, moment, date_now, context=None):
        categ_id = sale_order_line.product_id.delivery_categ_id
        if not categ_id:
            return True
        return (
            date_now +
            timedelta(days=categ_id.sale_delay) +
            timedelta(hours=moment.offset)) <=\
            datetime.strptime(moment.min_delivery_date, '%Y-%m-%d %H:%M:%S')

    # Field Functions Section
    def _get_order(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for sdm in self.browse(cr, uid, ids, context=context):
            res[sdm.id] = {
                'valid_order_qty': 0,
                'order_qty': len(sdm.order_ids),
                'is_complete': False,
                'quota_description': _('No Orders'),
            }
            # Update valid Orders Quantity
            for order in sdm.order_ids:
                if order.state not in ('draft', 'cancel'):
                    res[sdm.id]['valid_order_qty'] += 1

            # Update Is Complete Field
            if sdm.max_order_qty:
                res[sdm.id]['is_complete'] = (
                    res[sdm.id]['valid_order_qty'] >= sdm.max_order_qty)

            # Update Quota Description Field
            if sdm.max_order_qty:
                res[sdm.id]['quota_description'] = _('%d / %d Orders') % (
                    res[sdm.id]['valid_order_qty'], sdm.max_order_qty)
            elif res[sdm.id]['valid_order_qty']:
                res[sdm.id]['quota_description'] = _('%d Order(s)') % (
                    res[sdm.id]['valid_order_qty'])
        return res

    def _get_picking(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        sp_obj = self.pool['stock.picking']
        for sdm in self.browse(cr, uid, ids, context=context):
            order_ids = [x.id for x in sdm.order_ids]
            picking_ids = sp_obj.search(cr, uid, [
                ('sale_id', 'in', order_ids)], context=context)
            valid_picking_ids = sp_obj.search(cr, uid, [
                ('sale_id', 'in', order_ids),
                ('state', 'not in', ('draft', 'cancel'))], context=context)
            res[sdm.id] = {
                'picking_ids': picking_ids,
                'picking_qty': len(picking_ids),
                'valid_picking_qty': len(valid_picking_ids),
            }
        return res

    def _get_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for sdm in self.browse(cr, uid, ids, context=context):
            res[sdm.id] = sdm.min_delivery_date.split(' ')[0]
        return res

    # Columns Section
    _columns = {
        'name': fields.function(
            _get_name, type='char', string='Name', store={
                'sale.delivery.moment': (
                    lambda self, cr, uid, ids, context=None: ids,
                    ['min_delivery_date'], 10),
            }),
        'company_id': fields.many2one(
            'res.company', string='Company', required=True, readonly=True,
            select=True),
        'delivery_categ_id': fields.many2one(
            'sale.delivery.category', 'Delivery Category', required=True,
            select=True),
        'min_delivery_date': fields.datetime(
            string='Minimum date for the Delivery', required=True,
            select=True),
        'max_delivery_date': fields.datetime(
            string='Maximum date for the Delivery', required=True,
            select=True),
        'description': fields.text('Description'),
        'order_ids': fields.one2many(
            'sale.order', 'delivery_moment_id', 'Sale Orders', readonly=True),
        'order_qty': fields.function(
            _get_order, type='integer', multi='order',
            string='Sale Orders Quantity'),
        'valid_order_qty': fields.function(
            _get_order, type='integer', multi='order',
            string='Valid Sale Orders Quantity'),
        'is_complete': fields.function(
            _get_order, type='boolean', multi='order',
            string='Is Complete'),
        'max_order_qty': fields.integer(
            'Max Order Quantity'),
        'offset': fields.integer(
            'Offset (Hours)', required=True, help="Set positive value to"
            " increase delay or negative value to reduce delay."),
        'quota_description': fields.function(
            _get_order, type='char', multi='order',
            string='Quota Description'),
        'picking_ids': fields.function(
            _get_picking, type='one2many', multi='picking',
            relation='stock.picking', string='Delivery Orders'),
        'picking_qty': fields.function(
            _get_picking, type='integer', multi='picking',
            string='Delivery Orders Quantity'),
        'valid_picking_qty': fields.function(
            _get_picking, type='integer', multi='picking',
            string='Valid Delivery Orders Quantity'),
    }

    # Defaults Section
    _defaults = {
        'name': '/',
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
        'offset': 0,
    }

    # Constraint Section
    def _check_delivery_dates(self, cr, uid, ids, context=None):
        for sdm in self.browse(cr, uid, ids, context=context):
            if sdm.min_delivery_date >= sdm.max_delivery_date:
                return False
        return True

    _constraints = [
        (
            _check_delivery_dates,
            'Error ! The minimum Date of Delivery must be before the maximum'
            ' Date of Delivery.',
            ['min_delivery_date', 'max_delivery_date']),
    ]

    # Overload Section
    def unlink(self, cr, uid, ids, context=None):
        for sdm in self.browse(cr, uid, ids, context=context):
            if sdm.valid_order_qty:
                raise except_orm(
                    _('Error!'),
                    _("You can not delete this Delivery Moment because there"
                        " is %d Valid Sale Orders associated.\nPlease move"
                        " Sale orders on an other Delivery Moment and contact"
                        " your customers.") % (len(sdm.valid_order_qty)))
        return super(SaleDeliveryMoment, self).unlink(
            cr, uid, ids, context=context)
