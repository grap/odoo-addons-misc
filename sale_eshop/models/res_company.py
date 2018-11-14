# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

# from .model import _ESHOP_OPENERP_MODELS


class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'eshop.mixin']

    # Inherit Section
    _eshop_invalidation_type = 'single'

    _eshop_invalidation_fields = [
        'eshop_home_text_logged', 'eshop_home_text',
        'name', 'has_eshop', 'eshop_minimum_price', 'eshop_title',
        'eshop_url', 'website', 'eshop_list_view_enabled',
        'eshop_facebook_url', 'eshop_twitter_url', 'eshop_google_plus_url',
        'eshop_google_plus_url', 'eshop_instagram_url',
        'eshop_home_image', 'eshop_image_small',
        'eshop_vat_included', 'eshop_register_allowed',
        'manage_recovery_moment',
        'eshop_manage_unpacking',
    ]

    # Columns Section
    eshop_invalidation_cache_url = fields.Char(string='Invalidation Cache URL')

    has_eshop = fields.Boolean(string='Has eShop')

    eshop_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist', string='Pricelist Used on eShop')

    eshop_minimum_price = fields.Float(string='Minimum Price by eShop')

    eshop_manage_unpacking = fields.Boolean(string='Manage Unpacking on eShop')

    eshop_title = fields.Char(string='eShop Title')

    eshop_url = fields.Char(string='eShop URL')

    eshop_facebook_url = fields.Char(string='Facebook URL')

    eshop_twitter_url = fields.Char(string='Twitter URL')

    eshop_instagram_url = fields.Char(string='Instagram URL')

    eshop_google_plus_url = fields.Char(string='Google Plus URL')

    eshop_home_text = fields.Html(string='Text for the eShop Home Page')

    eshop_home_text_logged = fields.Html(
        string='Text for the eShop Home Page, when logged')

    eshop_home_image = fields.Binary(string='Image for the eShop Home Page')

    eshop_image_small = fields.Binary(string='Small Image for the eShop Menu')

    eshop_vat_included = fields.Boolean(string='VAT Included for eShop')

    eshop_register_allowed = fields.Boolean(
        string='Allow new customer to register on eShop')

    eshop_list_view_enabled = fields.Boolean(
        string='Provide a List view to realize quick purchase.')

    # Overload Section
    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        self._write_eshop_invalidate(vals)
        return super(ResCompany, self).write(vals)

    # Eshop APi - Section
    @api.model
    def get_eshop_model(self):
        return False
        # return _ESHOP_OPENERP_MODELS
