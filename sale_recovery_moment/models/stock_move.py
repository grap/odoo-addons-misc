# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Column Section
    prepare_categ_id = fields.Many2one(
        related='product_id.prepare_categ_id',
        comodel_name='product.prepare.category', store=True,
        string='Prepare Category', readonly=True)

    # Overload Section
    @api.model
    def _prepare_picking_assign(self, move):
        res = super(StockMove, self)._prepare_picking_assign(move)
        res.update({
            'recovery_moment_id':
            move.procurement_id.group_id.recovery_moment_id.id,
        })
        return res
