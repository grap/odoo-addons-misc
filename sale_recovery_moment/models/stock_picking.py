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
