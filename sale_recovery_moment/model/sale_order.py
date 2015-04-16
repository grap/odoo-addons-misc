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
from openerp import SUPERUSER_ID


class SaleOrder(Model):
    _inherit = 'sale.order'

    # Overload Section
    def _prepare_order_picking(self, cr, uid, order, context=None):
        """Set the moment id of the sale.order to the new stock.picking.out
        created."""
        res = super(SaleOrder, self)._prepare_order_picking(
            cr, uid, order, context=context)
        res['moment_id'] = order.moment_id.id
        return res

    def _prepare_order_line_move(
            self, cr, uid, order, line, picking_id, date_planned,
            context=None):
        """"Change 'date_expected' of the stock.move generated during sale
        confirmation, to order the moves depending of the
        product.prepare.category. This is tricky, we just add a second by
        sequence quantity of the prepare_categ_id of the current product
        line."""
        res = super(SaleOrder, self)._prepare_order_line_move(
            cr, uid, order, line, picking_id, date_planned, context=context)
        ppc_obj = self.pool['product.prepare.category']

        # Note: We access by SUPERUSER_ID, to avoid access restriction
        # if the user who valid the sale order is not part of
        # recovery groups
        if line.product_id and line.product_id.prepare_categ_id:
            ppc_offset_id = ppc_obj.search(
                cr, SUPERUSER_ID, [], limit=1, order='sequence desc')[0]
            ppc_offset = ppc_obj.browse(
                cr, SUPERUSER_ID, ppc_offset_id,
                context=context).sequence + 1
            ppc_sequence = ppc_obj.browse(
                cr, SUPERUSER_ID, line.product_id.prepare_categ_id.id,
                context=context).sequence
            res['date_expected'] = datetime.strptime(
                res['date_expected'], '%Y-%m-%d %H:%M:%S') +\
                timedelta(seconds=(ppc_offset - ppc_sequence))
        return res

    def create(self, cr, uid, vals, context=None):
        self._set_requested_date_from_moment_id(
            cr, uid, vals, context=context)
        return super(SaleOrder, self).create(
            cr, uid, vals, context=None)

    def write(self, cr, uid, ids, vals, context=None):
        self._set_requested_date_from_moment_id(
            cr, uid, vals, context=context)
        res = super(SaleOrder, self).write(
            cr, uid, ids, vals, context=None)
        return res

    # Custom Section
    def _set_requested_date_from_moment_id(self, cr, uid, vals, context=None):
        srm_obj = self.pool['sale.recovery.moment']
        if vals.get('moment_id', False):
            srm = srm_obj.browse(
                cr, uid, vals.get('moment_id'), context=context)
            vals.pop('requested_date', False)
            vals['requested_date'] = srm.min_recovery_date

    # Column Section
    _columns = {
        'moment_id': fields.many2one(
            'sale.recovery.moment', 'Recovery Moment',
            readonly=True, states={'draft': [('readonly', False)]}),
        'group_id': fields.related(
            'moment_id', 'group_id', type='many2one',
            relation='sale.recovery.moment.group',
            string='Recovery Moment Group', readonly=True),
    }
