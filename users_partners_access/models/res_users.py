# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Overload Section
    @api.model
    def create(self, vals):
        user = super(ResUsers, self).create(vals)
        user.partner_id._disable_users_partners()
        return user
