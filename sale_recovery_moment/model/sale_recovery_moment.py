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


class sale_recovery_moment(Model):
    _description = 'Recovery Moment'
    _name = 'sale.recovery.moment'
    _order = 'recovery_date, min_recovery_time, place_id'

    # Field Functions Section
    def _get_duration(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            res[srm.id] = srm.max_recovery_time - srm.min_recovery_time
        return res

    def _get_min_recovery_date(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            date = datetime.strptime(srm.recovery_date, '%Y-%m-%d')
            res[srm.id] = date + timedelta(
                hours=srm.min_recovery_time)
        return res

    def _get_max_recovery_date(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            date = datetime.strptime(srm.recovery_date, '%Y-%m-%d')
            res[srm.id] = date + timedelta(
                hours=srm.max_recovery_time)
        return res

    def _get_order_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            res[srm.id] = len(srm.order_ids)
        return res

    def _get_complete_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srm in self.browse(cr, uid, ids, context):
            address_format = srm.country_id \
                and srm.country_id.address_format \
                or "%(street)s\n%(street2)s\n%(city)s %(state_code)s" \
                " %(zip)s\n%(country_name)s"
            args = {
                'street': srm.street and srm.street or '',
                'street2': srm.street2 and srm.street2 or '',
                'zip': srm.zip and srm.zip or '',
                'city': srm.city and srm.city or '',
                'state_code': srm.state_id and srm.state_id.code or '',
                'state_name': srm.state_id and srm.state_id.name or '',
                'country_code': srm.country_id and srm.country_id.code or '',
                'country_name': srm.country_id and srm.country_id.name or '',
            }
            res[srm.id] = srm.name + ' - ' \
                + (address_format % args).replace('\n', ' ')
        return res

    def _get_picking(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        spo_obj = self.pool['stock.picking.out']
        for srm in self.browse(cr, uid, ids, context):
            order_ids = [x.id for x in srm.order_ids]
            picking_ids = spo_obj.search(cr, uid, [
                ('sale_id', 'in', order_ids)], context=context)
            res[srm.id] = {
                'picking_ids': picking_ids,
                'picking_qty': len(picking_ids)}
        return res

    # Columns Section
    _columns = {
        'name': fields.char(
            'Name', readonly=True, required=True),
        'place_id': fields.many2one(
            'sale.recovery.place', 'Place', required=True),
        'group_id': fields.many2one(
            'sale.recovery.moment.group', 'Recovery Moment Group',
            ondelete='cascade'),
        'company_id': fields.related(
            'group_id', 'company_id', type='many2one',relation='res.company',
            string='Company', store=True, readonly=True),
        'recovery_date': fields.date(
            'Date for the Recovery', required=True),
        'min_recovery_time': fields.float(
            'Minimum Recovery Time', required=True),
        'max_recovery_time': fields.float(
            'Maximum Recovery Time', required=True),
        'min_recovery_date': fields.function(
            _get_min_recovery_date, type='datetime',
            string='Minimum date for the Recovery'),
        'max_recovery_date': fields.function(
            _get_max_recovery_date, type='datetime',
            string='Minimum date for the Recovery'),
        'duration': fields.function(
            _get_duration, type='float', string='Duration (Hour)'),
        'description': fields.text('Description'),
        'order_ids': fields.one2many(
            'sale.order', 'moment_id', 'Sale Orders', readonly=True),
        'order_qty': fields.function(
            _get_order_qty, type='integer', string='Sale Orders Quantity'),
        'picking_ids': fields.function(
            _get_picking, type='one2many', multi='picking',
            relation='stock.picking.out', string='Stock Picking Quantity'),
        'picking_qty': fields.function(
            _get_picking, type='integer', multi='picking',
            string='Stock Picking Quantity'),
    }

    # Defaults Section
    _defaults = {
        'name': (
            lambda obj, cr, uid, context:
            obj.pool.get('ir.sequence').get(
                cr, uid, 'sale.recovery.moment')),
        'min_recovery_time': 8.0,
        'max_recovery_time': 16.0,
    }

    # Constraint Section
    def _check_recovery_times(self, cr, uid, ids, context=None):
        for srm in self.browse(cr, uid, ids, context=context):
            if srm.min_recovery_time >= srm.max_recovery_time:
                return False
        return True

    _constraints = [
        (
            _check_recovery_times,
            'Error ! The minimum Time of Recovery must be before the maximum'
            ' Time of Recovery.',
            ['min_recovery_time', 'max_recovery_time']),
    ]
