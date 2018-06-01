# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models


class SaleRecoveryMomentGroupWizardDuplicate(models.TransientModel):
    _name = 'sale.recovery.moment.group.wizard.duplicate'

    # Defaults Section
    @api.model
    def _default_group_id(self):
        return self.env.context.get('active_id', False)

    # Columns Section
    group_id = fields.Many2one(
        'sale.recovery.moment.group', 'Group to Duplicate', required=True,
        default=_default_group_id)

    day_delay = fields.Integer(
        'Delay (Day)', required=True,
        help="Please set a positive number here.\n"
        "The wizard will duplicate the current group moving forward"
        "all the dates by the delay.")

    short_name = fields.Char(string='Short Name', required=True)

    next_min_sale_date = fields.Date(
        string='Next Minimum Sale Date', required=True)

    next_max_sale_date = fields.Date('Next Maximum Sale', required=True)

    # View Sections
    @api.multi
    def duplicate_group(self):
        self.ensure_one()
        moment_obj = self.env['sale.recovery.moment']
        group_obj = self.env['sale.recovery.moment.group']

        # Create new group
        group_vals = {
            'short_name': self.short_name,
            'min_sale_date': self.next_min_sale_date,
            'max_sale_date': self.next_max_sale_date,
            'company_id': self.group_id.company_id.id,
        }
        new_group = group_obj.create(group_vals)

        # Create New Moment
        for moment in self.group_id.moment_ids:
            moment_vals = {
                'group_id': new_group.id,
                'min_recovery_date': (datetime.strptime(
                    moment.min_recovery_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=self.day_delay)).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                'max_recovery_date': (datetime.strptime(
                    moment.max_recovery_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=self.day_delay)).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                'place_id': moment.place_id.id,
                'max_order_qty': moment.max_order_qty,
                'description': moment.description,
            }
            moment_obj.create(moment_vals)

        action_data = self.env.ref(
            'sale_recovery_moment.action_sale_recovery_moment_group').read()[0]
        view = self.env.ref(
            'sale_recovery_moment.view_sale_recovery_moment_group_form')
        action_data['views'] = [(view.id, 'form')]
        action_data['res_id'] = new_group.id
        return action_data

    # View Section
    @api.onchange('group_id', 'day_delay')
    def onchange_day_delay(self):
        if self.day_delay and self.group_id:
            self.next_min_sale_date = (datetime.strptime(
                    self.group_id.min_sale_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=self.day_delay)).strftime(
                    '%Y-%m-%d')
            self.next_max_sale_date = (datetime.strptime(
                    self.group_id.max_sale_date, '%Y-%m-%d %H:%M:%S') +
                    relativedelta(days=self.day_delay)).strftime(
                    '%Y-%m-%d')
        else:
            self.next_min_sale_date = False
            self.next_max_sale_date = False
