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

from datetime import datetime, timedelta

from openerp.osv import fields
from openerp.osv.orm import Model


class SaleOrder(Model):
    _inherit = 'sale.order'

    _REMINDER_STATE_KEYS = [
        ('to_send', 'To Send'),
        ('do_not_send', 'Do Not Send'),
        ('sent', 'Sent'),
    ]

    # Column Section
    _columns = {
        'recovery_moment_id': fields.many2one(
            'sale.recovery.moment', 'Recovery Moment',
            readonly=True, states={'draft': [('readonly', False)]}),
        'recovery_group_id': fields.related(
            'recovery_moment_id', 'group_id', type='many2one',
            relation='sale.recovery.moment.group', readonly=True,
            string='Recovery Moment Group', store=True),
        'delivery_moment_id': fields.many2one(
            'sale.delivery.moment', 'Delivery Moment'),
        'reminder_state': fields.selection(
            _REMINDER_STATE_KEYS, 'State of the E-mail Reminder',
            required=True,
            help="To Send - The Reminder will be sent before the"
            " recovery date ;\n"
            "Do Not Send - The Reminder will not be sent before the"
            " recovery date ;\n"
            "Sent - The Reminder has been sent;"),
    }

    _defaults = {
        'reminder_state': 'do_not_send',
    }

    def copy(self, cr, uid, id, default=None, context=None):
        default = default and default or {}
        default['reminder_state'] = 'do_not_send'
        default['recovery_moment_id'] = False
        default['delivery_moment_id'] = False
        res = super(SaleOrder, self).copy(
            cr, uid, id, default, context=context)
        return res

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        self._set_requested_date_from_moment_id(
            cr, uid, vals, context=context)
        return super(SaleOrder, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        self._set_requested_date_from_moment_id(
            cr, uid, vals, context=context)
        res = super(SaleOrder, self).write(
            cr, uid, ids, vals, context=context)
        return res

    def _prepare_procurement_group(self, cr, uid, order, context=None):
        res = super(SaleOrder, self)._prepare_procurement_group(
            cr, uid, order, context=context)
        res.update({
            'recovery_moment_id': order.recovery_moment_id.id,
            'delivery_moment_id': order.delivery_moment_id.id,
        })
        return res

    def _prepare_order_line_move(
            self, cr, uid, order, line, picking_id, date_planned,
            context=None):
        """"Change 'date_expected' of the stock.move generated during sale
        confirmation, to set the one defined by the Recovery Moment"""
        res = super(SaleOrder, self)._prepare_order_line_move(
            cr, uid, order, line, picking_id, date_planned, context=context)

        if line.order_id.recovery_moment_id:
            # We take into account the min date of the recovery moment
            res['date_expected'] =\
                line.order_id.recovery_moment_id.min_recovery_date
        elif line.order_id.delivery_moment_id:
            # We take into account the min date of the delivery moment
            res['date_expected'] =\
                line.order_id.delivery_moment_id.min_delivery_date
        elif line.order_id.requested_date:
            # we take into account the expected_date of the sale
            res['date_expected'] = line.order_id.requested_date
        return res

    # Custom Section
    def _set_requested_date_from_moment_id(
            self, cr, uid, vals, context=None):
        srm_obj = self.pool['sale.recovery.moment']
        sdm_obj = self.pool['sale.delivery.moment']
        if vals.get('recovery_moment_id', False):
            srm = srm_obj.browse(
                cr, uid, vals.get('recovery_moment_id'), context=context)
            vals['requested_date'] = srm.min_recovery_date
        elif vals.get('delivery_moment_id', False):
            sdm = sdm_obj.browse(
                cr, uid, vals.get('delivery_moment_id'), context=context)
            vals['requested_date'] = sdm.min_delivery_date

    def _send_reminder_email(self, cr, uid, company_ids, hours, context=None):
        """Send a reminder for all customer that asked one reminder email
        before the customer has to recover his picking;
        This function can be croned;
        @param: company_ids : domain of the requests;
        @param: hours: number of hours before the mail will be sent;"""
        ru_obj = self.pool['res.users']
        imd_obj = self.pool['ir.model.data']
        et_obj = self.pool['email.template']
        et = imd_obj.get_object(
            cr, uid, 'sale', 'email_template_edi_sale')

        original_company_id = ru_obj.browse(
            cr, uid, uid, context=context).company_id.id
        for company_id in company_ids:
            ru_obj.write(cr, uid, [uid], {
                'company_id': company_id}, context=context)
            sent_so_ids = []
            so_ids = self.search(cr, uid, [
                ('reminder_state', '=', 'to_send'),
                ('recovery_moment_id', '!=', False),
                ('company_id', '=', company_id),
            ], context=context)
            for so in self.browse(cr, uid, so_ids, context=context):
                if datetime.now() + timedelta(hours=hours) > datetime.strptime(
                        so.recovery_moment_id.min_recovery_date,
                        '%Y-%m-%d %H:%M:%S'):
                    et_id = so.company_id.reminder_template\
                        and so.company_id.reminder_template.id or et.id
                    et_obj.send_mail(
                        cr, uid, et_id, so.id, True, context=context)
                    sent_so_ids.append(so.id)
            self.write(cr, uid, sent_so_ids, {
                'reminder_state': 'sent'}, context=context)

        ru_obj.write(cr, uid, [uid], {
            'company_id': original_company_id}, context=context)
