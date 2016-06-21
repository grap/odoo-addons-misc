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

{
    'name': 'Sale - eShop',
    'version': '8.0.1.0.0',
    'summary': "Allow connection to Odoo eShop Project",
    'category': 'Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'mail',
        'sale',
        'sale_recovery_moment',
        'simple_tax_sale',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir_module_category.yml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'data/email_template.xml',
        'view/wizard_view.xml',
        'view/wizard_action.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/res_partner.yml',
        'demo/eshop_category.xml',
        'demo/product_product.xml',
        'demo/product_uom.yml',
        'demo/res_users.yml',
        'demo/res_groups.yml',
    ],
    'installable': True,
}
