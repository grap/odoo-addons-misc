# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountTax(models.Model):
    _name = 'account.tax'
    _inherit = ['account.tax', 'eshop.mixin']

    # Inherit Section
    _eshop_invalidation_type = 'multiple'

    _eshop_invalidation_fields = ['eshop_description']

    # Field Section
    eshop_description = fields.Char(
        string='Description for the eShop', required=True, default='/')

    # Overload Section
    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        self._write_eshop_invalidate(vals)
        return super(AccountTax, self).write(vals)
