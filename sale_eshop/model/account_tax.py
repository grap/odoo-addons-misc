# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    eshop_description = fields.Char(
        string='Description for the eShop', required=True, default='/')
