# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Column Section
    recovery_moment_id = fields.Many2one(
        comodel_name='sale.recovery.moment', string='Recovery Moment')

    recovery_group_id = fields.Many2one(
        related='recovery_moment_id.group_id',
        comodel_name='sale.recovery.moment.group', store=True,
        string='Recovery Moment Group', readonly=True)

#    # Custom Section
#    def reorder_moves_by_category_and_name(
#            self, cr, uid, ids, context=None):
#        sm_obj = self.pool['stock.move']
#        ppc_obj = self.pool['product.prepare.category']
#        for picking in self.browse(cr, uid, ids, context=context):
#            # Get ordered categories
#            category_ids = ppc_obj.search(
#                cr, uid, [], order='sequence', context=context)
#            product_list = {x: [] for x in (category_ids + [0])}

#            # Load moves by categories
#            for sm in picking.move_lines:
#                if sm.product_id.prepare_categ_id:
#                    product_list[
#                        sm.product_id.prepare_categ_id.id].append(
#                        sm.product_id.id)
#                else:
#                    product_list[0].append(sm.product_id.id)
#            count = 0

#            # Write sequence, depending of category.sequence and product_id
#            for category_id in category_ids + [0]:
#                sm_ids = sm_obj.search(
#                    cr, uid, [
#                        ('picking_id', '=', picking.id),
#                        ('product_id', 'in', product_list[category_id]),
#                    ], order='product_id', context=context)
#                for sm_id in sm_ids:
#                    count += 1
#                    sm_obj.write(
#                        cr, uid, sm_id, {'sequence': count}, context=context)
