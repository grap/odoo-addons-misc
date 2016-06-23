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

import requests

from openerp import api
from openerp.osv.osv import except_osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


#    Define models used by eshop. Format.
#    'model.name' : {
#        'type': 'single' / 'multiple',
#        'fields': ['field_1', 'field_2']
#    }
#    If a model is defined in this list, all write action will call an
#    invalidation call to the according eshop (or eshops) to mention that
#    the model should be reloaded.

#    'fields' mentions wich fields raise invalidation call.

#    if type is 'single', only one invalidation will be called.
#    if type is 'multiple', all eshop will be called.
_ESHOP_OPENERP_MODELS = {
    # 'single' type Models
    'product.product': {
        'type': 'single',
        'fields': [
            'name', 'uom_id', 'image', 'image_medium', 'list_price',
            'eshop_category_id', 'label_ids', 'eshop_minimum_qty',
            'eshop_rounded_qty', 'origin_description', 'maker_description',
            'fresh_category', 'eshop_description', 'country_id',
            'department_id', 'default_code', 'delivery_categ_id',
            'eshop_taxes_description', 'eshop_unpack_qty',
            'eshop_unpack_surcharge'],
    },
    'res.company': {
        'type': 'single',
        'fields': [
            'eshop_home_text_logged', 'eshop_home_text',
            'name', 'has_eshop', 'eshop_minimum_price', 'eshop_title',
            'eshop_url', 'website', 'eshop_list_view_enabled',
            'eshop_facebook_url', 'eshop_twitter_url', 'eshop_google_plus_url',
            'eshop_google_plus_url', 'eshop_instagram_url',
            'eshop_home_image', 'eshop_image_small',
            'eshop_vat_included', 'eshop_register_allowed',
            'manage_delivery_moment', 'manage_recovery_moment',
            'eshop_manage_unpacking',
        ],
    },
    'res.partner': {
        'type': 'single',
        'fields': [
            'name', 'lang', 'email', 'eshop_active', 'eshop_state',
            'phone', 'mobile', 'street', 'street2', 'zip', 'city',
            'delivery_categ_id', 'simple_tax_type',
        ],
    },
    'eshop.category': {
        'type': 'single',
        'fields': [
            'name', 'available_product_qty', 'child_qty', 'image_medium',
            'type', 'parent_id', 'product_ids', 'complete_name'],
    },
    'product.delivery.category': {
        'type': 'single',
        'fields': ['name'],
    },

    # 'multiple' type Models
    'account.tax': {
        'type': 'multiple',
        'fields': ['eshop_description'],
    },
    'product.label': {
        'type': 'multiple',
        'fields': ['name', 'code', 'image', 'image_small'],
    },
    'res.country': {
        'type': 'multiple',
        'fields': ['name'],
    },
    'res.country.department': {
        'type': 'multiple',
        'fields': ['name'],
    },
    'product.uom': {
        'type': 'multiple',
        'fields': ['id', 'name', 'eshop_description'],
    },
}


_eshop_backup_write_function = Model.write


def _invalidate_eshop(cache_url, model_name, item_id, fields):
    url = cache_url + model_name + '/' + str(item_id) + '/'\
        + ','.join(fields) + '/'
    req = requests.get(url, verify=False)
    if req.status_code != 200:
        raise except_osv(_('Error !'), _(
            "You can not change this values because the"
            " eShop datas can not be updated."
            " \n - Code : %s") % (req.status_code))


@api.multi
def new_write_function(self, vals):
    company_obj = self.env['res.company']

    res = _eshop_backup_write_function(
        self, vals)

    if 'has_eshop' not in company_obj._all_columns.keys():
        # The module is not installed
        return res

    eshop_model = _ESHOP_OPENERP_MODELS.get(self._name, False)
    if not eshop_model:
        # The model is not synchronised with an eShop
        return res

    eshop_fields = eshop_model['fields']
    update_fields = vals.keys()
    intersec_fields = [x for x in eshop_fields if x in update_fields]
    if not intersec_fields:
        # No fields synchronised has changed
        return res

    # Some fields are loaded and cached by the eShop
    if eshop_model['type'] == 'single':
        for item in self:
            if self._name == 'res.company' and item.has_eshop:
                _invalidate_eshop(
                    item.eshop_invalidation_cache_url, self._name, item.id,
                    intersec_fields)

            elif self._name != 'res.company' and item.company_id.has_eshop:
                _invalidate_eshop(
                    item.company_id.eshop_invalidation_cache_url, self._name,
                    item.id, intersec_fields)

            else:
                # Company has no eShop
                return res

    if eshop_model['type'] == 'multiple':
        for company in company_obj.sudo().search([('has_eshop', '=', True)]):
            for id in self.ids:
                _invalidate_eshop(
                    company.eshop_invalidation_cache_url, self._name,
                    id, intersec_fields)

    return res


Model.write = new_write_function
