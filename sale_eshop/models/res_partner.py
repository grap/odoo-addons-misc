# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import random
import string

from openerp import api, exceptions, fields, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'eshop.mixin']

    # Inherit Section
    _eshop_invalidation_type = 'single'

    _eshop_invalidation_fields = [
        'name', 'lang', 'email', 'eshop_active', 'eshop_state',
        'phone', 'mobile', 'street', 'street2', 'zip', 'city',
        'simple_tax_type',
    ]

    _PASSWORD_LENGTH = 6
    _PASSWORD_CHARS = string.ascii_letters + '23456789'

    _ESHOP_STATE_SELECTION = [
        ('disabled', 'Disabled'),
        ('email_to_confirm', 'EMail To Confirm'),
        ('first_purchase', 'First Purchase'),
        ('enabled', 'Enabled'),
    ]

    # Columns Section
    eshop_password = fields.Char(string='Password on eShop', readonly=True)

    eshop_state = fields.Selection(
        selection=_ESHOP_STATE_SELECTION, string='State on eShop',
        readonly=True, default='disabled')

    eshop_active = fields.Boolean(
        string='Can buy on eShop', store=True, compute='_compute_eshop_active',
        readonly=True)

    # Compute Section
    @api.multi
    @api.depends('eshop_state')
    def _compute_eshop_active(self):
        for partner in self:
            partner.eshop_active =\
                partner.eshop_state in ['first_purchase', 'enabled']

    # Overload Section
    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        self._write_eshop_invalidate(vals)
        return super(ResPartner, self).write(vals)

    # View - Section
    @api.multi
    def button_enable_eshop(self):
        self.write({'eshop_state': 'enabled'})

    @api.multi
    def button_disable_eshop(self):
        self.write({
            'eshop_password': False,
            'eshop_state': 'disabled',
        })

    @api.multi
    def button_generate_credentials(self):
        self._generate_credentials()

    @api.multi
    def button_send_credentials(self):
        self._send_credentials()

    # Eshop API - Section
    @api.model
    def login(self, login, password):
        ResUsers = self.env['res.users']
        if not password:
            return False
        res = self.search([
            ('email', '=', login),
            ('eshop_password', '=', password),
            ('eshop_state', 'in', ['first_purchase', 'enabled']),
        ])
        if len(res) == 1:
            return res[0].id
        try:
            ResUsers.sudo().check_credentials(password)
            res = self.search([
                ('email', '=', login),
                ('eshop_active', '=', True),
            ])
            if len(res) == 1:
                return res[0].id
            else:
                return False
        except exceptions.AccessDenied:
            return False

    @api.model
    def create_from_eshop(self, vals):
        vals.update({
            'name': vals['first_name'] + ' ' + vals['last_name'],
            'eshop_state': 'email_to_confirm',
        })
        vals.pop('first_name', False)
        vals.pop('last_name', False)
        # Create partner
        partner = self.create(vals)
        # Send an email
        return partner._send_credentials()

    # Private Section
    @api.multi
    def _send_credentials(self):
        # TODO
        # imd_obj = self.pool['ir.model.data']
        # et_obj = self.pool['email.template']
        # et = imd_obj.get_object(
        #     cr, uid, 'sale_eshop', 'eshop_send_crendential_template')

        # for rp in self.browse(cr, uid, ids, context=context):
        #     et_obj.send_mail(cr, uid, et.id, rp.id, True, context=context)
        return True

    @api.multi
    def _generate_credentials(self):
        for partner in self:
            random.seed = (os.urandom(1024))
            password = ''.join(random.choice(
                self._PASSWORD_CHARS) for i in range(self._PASSWORD_LENGTH))
            partner.write({
                'eshop_password': password,
                'eshop_state': 'enabled'})

    # Overwrite section
    @api.model
    def _get_eshop_domain(self):
        return [('eshop_active', '=', True)]
