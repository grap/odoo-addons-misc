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


from openerp import SUPERUSER_ID
from openerp.osv.osv import except_osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


_ESHOP_OPENERP_MODELS = {
    'product.label': {
        'type': 'multiple',
        'fields': ['name', 'code', 'image_small', 'image'],
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
        'fields': ['name', 'eshop_description'],
    },
    'res.company': {
        'type': 'single',
        'fields': [
            'name', 'has_eshop', 'eshop_minimum_price', 'eshop_title',
            'eshop_url',
            'eshop_facebook_url', 'eshop_twitter_url', 'eshop_google_plus_url',
            'eshop_home_text', 'eshop_home_image', 'eshop_image_small',
            'eshop_vat_included', 'eshop_register_allowed',
            'eshop_list_view_enabled',
            'manage_delivery_moment', 'manage_recovery_moment',
        ],
    },
}



_eshop_backup_write_function = Model.write

def new_write_function(self, cr, uid, ids, vals, context=None):
    res = _eshop_backup_write_function(
        self, cr, uid, ids, vals, context=context)
    eshop_model = _ESHOP_OPENERP_MODELS.get(self._name, False)
    if eshop_model:
        user_obj = self.pool['res.users']
        company_obj = self.pool['res.company']
        # It's a model loaded and cached by the eShop
        eshop_fields = eshop_model['fields']
        
        update_fields = vals.keys()
        intersec_fields = [x for x in eshop_fields if x in update_fields]
        print "************"
        print eshop_fields
        print update_fields
        print intersec_fields
        if intersec_fields:
            # Some fields are loaded and cached by the eShop
            if eshop_model['type'] == 'single':
                company_ids = [x for x in [user_obj._get_company(
                            cr, uid, context=context)]
                                if x in company_obj.search(cr, SUPERUSER_ID, [('has_eshop', '=', True)], context=context)]
                if not company_ids:
                    raise except_osv(_('Error !'), _(
                        "You can not change this values because you have"
                        " not selected the good company."))
                
            else:
                company_ids = company_obj.search(
                    cr, SUPERUSER_ID, [('has_eshop', '=', True)],
                    context=context)
            print company_ids
            for company in company_obj.browse(
                    cr, SUPERUSER_ID, company_ids, context=context):
                for id in ids:
                    url = company.eshop_invalidation_cache_url\
                        + self._name + '/' + str(id)
                    print url
                    # TODO IMPROVE ME, auth=('user', 'pass')
                    req = requests.get(url)
                    if req.status_code != 200:
                        raise except_osv(_('Error !'), _(
                            "You can not change this values because the"
                            " eShop is unreachable."))

    return res

Model.write = new_write_function
