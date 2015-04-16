# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
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
from dateutil.relativedelta import relativedelta

from openerp.osv import fields
from openerp.osv.orm import TransientModel


class sale_recovery_moment_group_wizard_duplicate(TransientModel):
    _name = 'sale.recovery.moment.group.wizard.duplicate'

    def duplicate_group(self, cr, uid, ids, context=None):
        imd_obj = self.pool['ir.model.data']
        srm_obj = self.pool['sale.recovery.moment']
        srmg_obj = self.pool['sale.recovery.moment.group']
        iaaw_obj = self.pool['ir.actions.act_window']
        srmg_ids = []
        for srmgwd in self.browse(cr, uid, ids, context=context):
            # Create new group
            vals = {
                'short_name': srmgwd.short_name,
                'min_sale_date': (datetime.strptime(
                    srmgwd.group_id.min_sale_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=srmgwd.day_delay)).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                'max_sale_date': (datetime.strptime(
                    srmgwd.group_id.max_sale_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=srmgwd.day_delay)).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                'shop_id': srmgwd.group_id.shop_id.id,
                'company_id': srmgwd.group_id.company_id.id,
            }
            srmg_id = srmg_obj.create(cr, uid, vals, context=context)
            # Create New Moment
            for srm in srmgwd.group_id.moment_ids:
                vals = {
                    'group_id': srmg_id,
                    'min_recovery_date': (datetime.strptime(
                        srm.min_recovery_date, '%Y-%m-%d %H:%M:%S') +
                        relativedelta(days=srmgwd.day_delay)).strftime(
                        '%Y-%m-%d %H:%M:%S'),
                    'max_recovery_date': (datetime.strptime(
                        srm.max_recovery_date, '%Y-%m-%d %H:%M:%S') +
                        relativedelta(days=srmgwd.day_delay)).strftime(
                        '%Y-%m-%d %H:%M:%S'),
                    'place_id': srm.place_id.id,
                    'max_order_qty': srm.max_order_qty,
                    'description': srm.description,
                }
                srm_obj.create(cr, uid, vals, context=context)
            srmg_ids.append(srmg_id)

        # Get Action to return to the Client
        iaaw_id = imd_obj.get_object_reference(
            cr, uid, 'sale_recovery_moment',
            'action_sale_recovery_moment_group')[1]
        res = iaaw_obj.read(cr, uid, [iaaw_id], context=context)[0]

        # Choose the view_mode accordingly
        if len(srmg_ids) > 1:
            res['domain'] =\
                "[('id','in',[" + ','.join(map(str, srmg_ids)) + "])]"
        else:
            res['views'] = [(False, 'form')]
            res['res_id'] = srmg_ids[0]

        return res

    _columns = {
        'group_id': fields.many2one(
            'sale.recovery.moment.group', 'Group to Duplicate', required=True,
            readonly=True),
        'day_delay': fields.integer(
            'Delay (Day)', required=True,
            help="Please set a positive number here.\n"
            "The wizard will duplicate the current group moving forward"
            "all the dates by the delay."),
        'short_name': fields.char(
            'Short Name', required=True),
        'next_min_sale_date': fields.date(
            'Next Minimum date for the Sale', readonly=True),
        'next_max_sale_date': fields.date(
            'Next Maximum date for the Sale', readonly=True),
    }

    _defaults = {
        'group_id': lambda self, cr, uid, ctx: ctx and ctx.get(
            'active_id', False) or False
    }

    # View Section
    def onchange_day_delay(
            self, cr, uid, ids, group_id, day_delay, next_min_sale_date,
            next_max_sale_date, context=None):
        if day_delay and group_id:
            group = self.pool['sale.recovery.moment.group'].browse(
                cr, uid, group_id, context)
            return {'value': {
                'next_min_sale_date': (datetime.strptime(
                    group.min_sale_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=day_delay)).strftime(
                    '%Y-%m-%d'),
                'next_max_sale_date': (datetime.strptime(
                    group.max_sale_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=day_delay)).strftime(
                    '%Y-%m-%d'),
            }}
        return {'value': {
            'next_min_sale_date': False,
            'next_max_sale_date': False}}
