# -*- encoding: utf-8 -*-
##############################################################################
#
#    User Partners Access module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import SUPERUSER_ID
from openerp.osv.orm import Model
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class res_partner(Model):
    _inherit = 'res.partner'

    # Custom section
    def _init_users_partners(self, cr, uid, ids=None, context=None):
        user_obj = self.pool['res.users']
        user_ids = user_obj.search(
            cr, uid, [('active', 'in', [True, False])], context=context)
        users = user_obj.browse(cr, uid, user_ids, context=context)
        partner_ids = [user.partner_id.id for user in users]
        self._disable_users_partners(cr, uid, partner_ids, context=context)

    def _check_users_partners_access(self, cr, uid, ids, vals, context=None):
        user_obj = self.pool['res.users']
        # We use SUPERUSER_ID to be sure to not skip some users, due to
        # some custom access rules deployed on databases
        users = user_obj.search(
            cr, SUPERUSER_ID, [
                ('active', 'in', [True, False]), ('partner_id', 'in', ids)],
            context=context)
        if len(users) != 0:
            # Check if current user has correct access right
            if not self.pool['res.users'].has_group(
                    cr, uid, 'base.group_erp_manager'):
                raise except_osv(_("Access Forbiden !"), _(
                    "You must be part of the group Administration / Access"
                    " Rights to update partners associated to users."))

    def _disable_users_partners(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'active': False,
            'company_id': False,
            'customer': False,
            'supplier': False})

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        res = super(res_partner, self).create(cr, uid, vals, context=context)
        self._check_users_partners_access(
            cr, uid, [res], vals, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        res = super(res_partner, self).write(
            cr, uid, ids, vals, context=context)
        self._check_users_partners_access(
            cr, uid, ids, vals, context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        self._check_users_partners_access(
            cr, uid, ids, {}, context=context)
        res = super(res_partner, self).unlink(
            cr, uid, ids, context=context)
        return res
