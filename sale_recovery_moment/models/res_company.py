# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    reminder_template = fields.Many2one(
        comodel_name='email.template', string='Template of Reminder Mail')

    manage_recovery_moment = fields.Boolean(string='Manage Recovery Moment')
