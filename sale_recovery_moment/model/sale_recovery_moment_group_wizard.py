# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Food Module for Odoo
#    Copyright (C) 2012-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class sale_recovery_moment_group_wizard(TransientModel):
    _name = 'sale.recovery.moment.group.wizard'

    # Fields Function Section
    def _get_group_id(self, cr, uid, context=None):
        return context['active_id']

    def _get_line_ids(self, cr, uid, context=None):
        res = []
        srmg_id = context['active_id']
        srmg_obj = self.pool['sale.recovery.moment.group']
        so_obj = self.pool['sale.order']
        sol_obj = self.pool['sale.order.line']
        pp_obj = self.pool['product.product']
        srmg = srmg_obj.browse(cr, uid, srmg_id, context=context)
        srm_ids = [line_id.id for line_id in srmg.moment_ids]
        so_ids = so_obj.search(cr, uid, [
            ('moment_id', 'in', srm_ids), ('state', '!=', 'cancel')],
            context=context)
        sol_ids = sol_obj.search(cr, uid, [
            ('order_id', 'in', so_ids)], context=context)
        res_pp = {}
        for sol in sol_obj.browse(cr, uid, sol_ids, context=context):
            if sol.product_id.id not in res_pp.keys():
                res_pp[sol.product_id.id] = 0.0
                res_pp[sol.product_id.id] += sol.product_uom_qty
            pass
        for key, value in res_pp.items():
            pp = pp_obj.browse(cr, uid, key, context=context)
            res.append((0, 0, {
                'product_id': key,
                'confirmed_qty': value,
                'qty_available': pp.qty_available,
                'incoming_qty': pp.incoming_qty,
                'outgoing_qty': pp.outgoing_qty,
                }))
        return res

    # Columns Section
    _columns = {
        'name': fields.char('Name'),
        'group_id': fields.many2one(
            'sale.recovery.moment.group', 'Moment Group'),
        'line_ids': fields.one2many(
            'sale.recovery.moment.group.wizard.line', 'wizard_id',
            'Products', readonly=True),
    }

    # Default values Section
    _defaults = {
        'name': '/',
        'group_id': _get_group_id,
        'line_ids': _get_line_ids,
    }
