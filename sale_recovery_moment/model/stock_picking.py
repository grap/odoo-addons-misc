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


from openerp.osv import fields
from openerp.osv.orm import Model


class stock_picking(Model):
    _inherit = 'stock.picking'

    # Column Section
    _columns = {
        'recovery_moment_id': fields.many2one(
            'sale.recovery.moment', 'Recovery Moment'),
        'recovery_group_id': fields.related(
            'recovery_moment_id', 'group_id', type='many2one',
            relation='sale.recovery.moment.group', store=True,
            string='Recovery Moment Group', readonly=True),
        'delivery_moment_id': fields.many2one(
            'sale.delivery.moment', 'Delivery Moment'),
    }

    # Custom Section
    def reorder_moves_by_category_and_name(
            self, cr, uid, ids, context=None):
        sm_obj = self.pool['stock.move']
        ppc_obj = self.pool['product.prepare.category']
        for picking in self.browse(cr, uid, ids, context=context):
            # Get ordered categories
            category_ids = ppc_obj.search(
                cr, uid, [], order='sequence', context=context)
            product_list = {x: [] for x in (category_ids + [0])}

            # Load moves by categories
            for sm in picking.move_lines:
                if sm.product_id.prepare_categ_id:
                    product_list[
                        sm.product_id.prepare_categ_id.id].append(
                        sm.product_id.id)
                else:
                    product_list[0].append(sm.product_id.id)
            count = 0

            # Write sequence, depending of category.sequence and product_id
            for category_id in category_ids + [0]:
                sm_ids = sm_obj.search(
                    cr, uid, [
                        ('picking_id', '=', picking.id),
                        ('product_id', 'in', product_list[category_id]),
                    ], order='product_id', context=context)
                for sm_id in sm_ids:
                    count += 1
                    sm_obj.write(
                        cr, uid, sm_id, {'sequence': count}, context=context)
