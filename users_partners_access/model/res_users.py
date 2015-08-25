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

from openerp.osv.orm import Model


class res_users(Model):
    _inherit = 'res.users'

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        partner_obj = self.pool['res.partner']
        res = super(res_users, self).create(cr, uid, vals, context=context)
        user = self.browse(cr, uid, res, context=context)
        partner_obj._disable_users_partners(
            cr, uid, [user.partner_id.id], context=context)
        return res
