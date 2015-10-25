# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - eShop for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

import os
import random
import string

from openerp.osv import fields
from openerp.osv.orm import Model


class ResPartner(Model):
    _inherit = 'res.partner'

    _PASSWORD_LENGTH = 6
    _PASSWORD_CHARS = string.ascii_letters + '23456789'

    _ESHOP_STATE_KEYS = [
        ('disabled', 'Disabled'),
        ('email_to_confirm', 'EMail To Confirm'),
        ('first_purchase', 'First Purchase'),
        ('enabled', 'Enabled'),
    ]

    def _get_eshop_active(
            self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for rp in self.browse(cr, uid, ids, context=context):
            res[rp.id] = rp.eshop_state in ['first_purchase', 'enabled']
        return res

    # Columns Section
    _columns = {
        'eshop_password': fields.char('Password on eShop', readonly=True),
        'eshop_state': fields.selection(
            _ESHOP_STATE_KEYS, 'State on eShop', readonly=True, required=True),
        'eshop_active': fields.function(
            _get_eshop_active, string='Can buy on eShop', store=True,
            readonly=True),
    }

    _defaults = {
        'eshop_state': 'disabled',
    }

    # Public Custom Section
    def login(self, cr, uid, login, password, context=None):
        if not password:
            return False
        res = self.search(cr, uid, [
            ('email', '=', login),
            ('eshop_password', '=', password),
            ('eshop_state', 'in', ['first_purchase', 'enabled']),
        ], context=context)
        if len(res) == 1:
            return res[0]
        else:
            return False

    def create_from_eshop(self, cr, uid, vals, context=None):
        vals.update({
            'name': vals['first_name'] + ' ' + vals['last_name'],
            'eshop_state': 'email_to_confirm',
        })
        vals.pop('first_name', False)
        vals.pop('last_name', False)
        # Create partner
        res = self.create(cr, uid, vals, context=context)
        # Send an email
        self.send_credentials(cr, uid, [res], context=context)

    def send_credentials(self, cr, uid, ids, context=None):
        context = context or {}
        imd_obj = self.pool['ir.model.data']
        et_obj = self.pool['email.template']
        ss_obj = self.pool['sale.shop']
        et = imd_obj.get_object(
            cr, uid, 'sale_eshop', 'eshop_send_crendential_template')

        for rp in self.browse(cr, uid, ids, context=context):
            ss_ids = ss_obj.search(cr, uid, [
                ('company_id', '=', rp.company_id.id),
                ('eshop_url', '!=', False),
            ], context=context)
            ctx = context.copy()
            if ss_ids:
                ctx['eshop_url'] = ss_obj.browse(
                    cr, uid, ss_ids[0], context=context).eshop_url
            et_obj.send_mail(
                cr, uid, et.id, rp.id, True, context=ctx)
        return True

    # View Function Section
    def button_confirm_eshop(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'eshop_state': 'enabled'}, context=context)

    def button_disable_eshop(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'eshop_password': False,
            'eshop_state': 'disabled'}, context=context)

    def button_generate_send_password(self, cr, uid, ids, context=None):
        for rp in self.browse(cr, uid, ids, context=context):
            random.seed = (os.urandom(1024))
            password = ''.join(random.choice(
                self._PASSWORD_CHARS) for i in range(self._PASSWORD_LENGTH))
            self.write(cr, uid, ids, {
                'eshop_password': password,
                'eshop_state': 'enabled'}, context=context)
        self.send_credentials(cr, uid, ids, context=context)
        return True
