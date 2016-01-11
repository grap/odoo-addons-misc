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

from .model import _ESHOP_OPENERP_MODELS

from openerp.osv import fields
from openerp.osv.orm import Model


class ResCompany(Model):
    _inherit = 'res.company'

    def GetEshopModel(self, cr, uid, context=None):
        return _ESHOP_OPENERP_MODELS

    # Columns Section
    _columns = {
        'eshop_invalidation_cache_url': fields.char(
            'Invalidation Cache URL'),
        'has_eshop': fields.boolean(
            'Has eShop'),
        'eshop_pricelist_id': fields.many2one(
            'product.pricelist', 'Pricelist Used on eShop'),
        'eshop_minimum_price': fields.float(
            'Minimum Price by eShop'),
        'eshop_manage_unpacking': fields.boolean(
            'Manage Unpacking on eShop'),
        'eshop_title': fields.char(
            'eShop Title'),
        'eshop_url': fields.char(
            'eShop URL', oldname="eshop_website"),
        'eshop_facebook_url': fields.char(
            'Facebook URL'),
        'eshop_twitter_url': fields.char(
            'Twitter URL'),
        'eshop_instagram_url': fields.char(
            'Instagram URL'),
        'eshop_google_plus_url': fields.char(
            'Google Plus URL'),
        'eshop_home_text': fields.html(
            'Text for the eShop Home Page'),
        'eshop_home_text_logged': fields.html(
            'Text for the eShop Home Page, when logged'),
        'eshop_home_image': fields.binary(
            'Image for the eShop Home Page', oldname="eshop_image"),
        'eshop_image_small': fields.binary(
            'Small Image for the eShop Menu'),
        'eshop_vat_included': fields.boolean(
            'VAT Included for eShop'),
        'eshop_register_allowed': fields.boolean(
            'Allow new customer to register on eShop'),
        'eshop_list_view_enabled': fields.boolean(
            'Provide a List view to realize quick purchase.'),
    }
