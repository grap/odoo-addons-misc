# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, models
from openerp.exceptions import Warning as UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Overload Section
    @api.multi
    def write(self, vals):
        self._check_users_partners_access()
        return super(ResPartner, self).write(vals)

    @api.multi
    def unlink(self):
        self._check_users_partners_access()
        return super(ResPartner, self).unlink()

    # Custom section
    @api.multi
    def _disable_users_partners(self):
        self.write({
            'active': False,
            'company_id': False,
            'customer': False,
            'supplier': False,
        })

    @api.multi
    def _check_users_partners_access(self):
        # We use SUPERUSER_ID to be sure to not skip some users, due to
        # some custom access rules deployed on databases
        ResUsers = self.env['res.users'].sudo()
        users = ResUsers.with_context(active_test=False).search([
            ('partner_id', 'in', self.ids)])
        if len(users) != 0:
            # Check if current user has correct access right
            if not self.env.user.has_group('base.group_erp_manager'):
                raise UserError(_(
                    "You must be part of the group Administration / Access"
                    " Rights to update partners associated to"
                    " users.\n- %s") % ('\n- '.join(users.mapped('name'))))
