# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Column Section
    recovery_moment_id = fields.Many2one(
        comodel_name='sale.recovery.moment', string='Recovery Moment',
        copy=False, readonly=True, states={'draft': [('readonly', False)]})

    recovery_group_id = fields.Many2one(
        related='recovery_moment_id.group_id',
        comodel_name='sale.recovery.moment.group', readonly=True,
        string='Recovery Moment Group', store=True)

    # Overload Section
    @api.model
    def create(self, vals):
        self._set_requested_date_from_moment_id(vals)
        return super(SaleOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        self._set_requested_date_from_moment_id(vals)
        return super(SaleOrder, self).write(vals)

    @api.model
    def _prepare_procurement_group(self, order):
        res = super(SaleOrder, self)._prepare_procurement_group(order)
        res.update({
            'recovery_moment_id': order.recovery_moment_id.id,
        })
        return res

    @api.model
    def _prepare_order_line_move(self, order, line, picking_id, date_planned):
        """"Change 'date_expected' of the stock.move generated during sale
        confirmation, to set the one defined by the Recovery Moment"""
        res = super(SaleOrder, self)._prepare_order_line_move(
            order, line, picking_id, date_planned)

        if line.order_id.recovery_moment_id:
            # We take into account the min date of the recovery moment
            res['date_expected'] =\
                line.order_id.recovery_moment_id.min_recovery_date
        elif line.order_id.requested_date:
            # we take into account the expected_date of the sale
            res['date_expected'] = line.order_id.requested_date
        return res

    # Custom Section
    @api.model
    def _set_requested_date_from_moment_id(self, vals):
        moment_obj = self.env['sale.recovery.moment']
        if vals.get('recovery_moment_id', False):
            moment = moment_obj.browse(vals.get('recovery_moment_id'))
            vals['requested_date'] = moment.min_recovery_date
