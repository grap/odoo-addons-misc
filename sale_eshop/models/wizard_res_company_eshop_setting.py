# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

# from .model import _ESHOP_OPENERP_MODELS


class WizardResCompanyEshopSetting(models.TransientModel):
    _name = 'wizard.res.company.eshop.setting'

    # Columns Section
    company_id = fields.Many2one(
        comodel_name='res.company', required=True, readonly=True,
        default=lambda s: s._default_company_id())

    eshop_facebook_url = fields.Char(
        string='Facebook URL',
        default=lambda s: s._default_eshop_facebook_url())

    eshop_twitter_url = fields.Char(
        string='Twitter URL',
        default=lambda s: s._default_eshop_twitter_url())

    eshop_instagram_url = fields.Char(
        string='Instagram URL',
        default=lambda s: s._default_eshop_instagram_url())

    eshop_google_plus_url = fields.Char(
        string='Instagram URL',
        default=lambda s: s._default_eshop_google_plus_url())

    eshop_home_text = fields.Html(
        string='Text for the eShop Home Page',
        default=lambda s: s._default_eshop_home_text())

    # Default Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_eshop_facebook_url(self):
        return self.env.user.company_id.eshop_facebook_url

    @api.model
    def _default_eshop_twitter_url(self):
        return self.env.user.company_id.eshop_twitter_url

    @api.model
    def _default_eshop_instagram_url(self):
        return self.env.user.company_id.eshop_instagram_url

    @api.model
    def _default_eshop_google_plus_url(self):
        return self.env.user.company_id.eshop_google_plus_url

    @api.model
    def _default_eshop_home_text(self):
        return self.env.user.company_id.eshop_home_text

    # View Section
    @api.multi
    def button_apply_setting(self):
        self.ensure_one()
        self.company_id.sudo().write({
            'eshop_facebook_url': self.eshop_facebook_url,
            'eshop_twitter_url': self.eshop_twitter_url,
            'eshop_instagram_url': self.eshop_instagram_url,
            'eshop_google_plus_url': self.eshop_google_plus_url,
            'eshop_home_text': self.eshop_home_text,
        })
