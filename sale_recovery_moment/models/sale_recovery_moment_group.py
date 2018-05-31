# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError, ValidationError

import openerp.addons.decimal_precision as dp


class SaleRecoveryMomentGroup(models.Model):
    _name = 'sale.recovery.moment.group'
    _order = 'min_sale_date desc, name'

    # Defaults Section
    @api.model
    def _default_code(self):
        return self.env['ir.sequence'].get('sale.recovery.moment.group')

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    # Column Section
    code = fields.Char(
        string='Code', readonly=True, required=True, default=_default_code)

    short_name = fields.Char(string='Short Name', required=True)

    name = fields.Char(
        compute='_compute_name', string='Name', store=True)

    min_sale_date = fields.Datetime(
        string='Minimum date for the Sale', required=True)

    max_sale_date = fields.Datetime(
        string='Maximum date for the Sale', required=True)

    min_recovery_date = fields.Datetime(
        compute='_compute_recovery_date', multi='recovery_date',
        string='Minimum date for the Recovery', store=True)

    max_recovery_date = fields.Datetime(
        compute='_compute_recovery_date', multi='recovery_date',
        string='Maximum date for the Recovery', store=True)

    moment_ids = fields.One2many(
        comodel_name='sale.recovery.moment', inverse_name='group_id',
        string='Recovery Moments')

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', required=True)

    order_qty = fields.Integer(
        compute='_compute_order_multi', multi='order', store=True,
        string='Sale Orders Quantity')

    valid_order_qty = fields.Integer(
        compute='_compute_order_multi', multi='order', store=True,
        string='Valid Sale Orders Quantity')

    picking_qty = fields.Integer(
        compute='_compute_picking_multi', multi='picking', store=True,
        string='Delivery Orders Quantity')

    valid_picking_qty = fields.Integer(
        compute='_compute_picking_multi', multi='picking', store=True,
        string='Valid Delivery Orders Quantity')

    excl_total = fields.Float(
        compute='_compute_total_multi', multi='total', store=True,
        digits_compute=dp.get_precision('Account'),
        string='Total (VAT Excluded)')

    incl_total = fields.Float(
        compute='_compute_total_multi', multi='total', store=True,
        digits_compute=dp.get_precision('Account'),
        string='Total (VAT Included)')

    # Compute Section
    @api.multi
    @api.depends(
        'moment_ids.min_recovery_date', 'moment_ids.max_recovery_date')
    def _compute_recovery_date(self):
        for moment_group in self:
            if len(moment_group.moment_ids) > 0:
                moments = moment_group.moment_ids
                moment_group.min_recovery_date =\
                    min([x.min_recovery_date for x in moments])
                moment_group.max_recovery_date =\
                    min([x.max_recovery_date for x in moments])

    @api.multi
    @api.depends(
        'moment_ids.order_qty', 'moment_ids.valid_order_qty')
    def _compute_order_multi(self):
        for moment_group in self:
            moment_group.order_qty = sum(
                moment_group.mapped('moment_ids.order_qty'))
            moment_group.valid_order_qty = sum(
                moment_group.mapped('moment_ids.valid_order_qty'))

    @api.multi
    @api.depends(
        'moment_ids.picking_qty', 'moment_ids.valid_picking_qty')
    def _compute_picking_multi(self):
        for moment_group in self:
            moment_group.picking_qty = sum(
                moment_group.mapped('moment_ids.picking_qty'))
            moment_group.valid_picking_qty = sum(
                moment_group.mapped('moment_ids.valid_picking_qty'))

    @api.multi
    @api.depends('valid_order_qty')
    def _compute_total_multi(self):
        for moment_group in self:
            orders = moment_group.mapped('moment_ids.order_ids').filtered(
                lambda x: x.state not in ('draft', 'cancel'))
            moment_group.excl_total = sum(orders.mapped('amount_untaxed'))
            moment_group.incl_total = sum(orders.mapped('amount_total'))

    @api.multi
    @api.depends('code', 'short_name')
    def _compute_name(self):
        for moment_group in self:
            moment_group.name = '%s - %s' % (
                moment_group.code, moment_group.short_name)

    # Constraint Section
    @api.multi
    @api.constrains('min_sale_date', 'max_sale_date')
    def _check_sale_dates(self):
        for moment_group in self:
            if moment_group.min_sale_date >= moment_group.max_sale_date:
                raise ValidationError(_(
                    "The minimum Date of Sale must be before the maximum"
                    " Date of Sale."))

    # Overload Section
    def copy(self):
            raise UserError(_(
                "You can not duplicate by this way, please use the"
                " Duplicate Button in the Form view."))
