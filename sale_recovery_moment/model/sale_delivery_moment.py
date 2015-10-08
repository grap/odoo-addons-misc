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

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp.osv.orm import except_orm
from openerp.tools.translate import _


class SaleDeliveryMoment(Model):
    _name = 'sale.delivery.moment'

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
        spo_obj = self.pool['stock.picking.out']
        for sdm in self.browse(cr, uid, ids, context=context):
            order_ids = [x.id for x in sdm.order_ids]
            picking_ids = spo_obj.search(cr, uid, [
                ('sale_id', 'in', order_ids)], context=context)
            valid_picking_ids = spo_obj.search(cr, uid, [
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
            'res.company', string='Company', required=True, readonly=True),
        'delivery_categ_id': fields.many2one(
            'sale.delivery.category', 'Delivery Category', required=True),
        'min_delivery_date': fields.datetime(
            string='Minimum date for the Delivery', required=True),
        'max_delivery_date': fields.datetime(
            string='Maximum date for the Delivery', required=True),
        'description': fields.text('Description'),
        'order_ids': fields.one2many(
            'sale.order', 'moment_id', 'Sale Orders', readonly=True),
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
        'quota_description': fields.function(
            _get_order, type='char', multi='order',
            string='Quota Description'),
        'picking_ids': fields.function(
            _get_picking, type='one2many', multi='picking',
            relation='stock.picking.out', string='Delivery Orders'),
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
