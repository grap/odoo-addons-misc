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
    'version': '0.1',
    'summary': "Allow connection to Odoo eShop Project",
    'category': 'Sale',
    'description': """
Allow connection to Odoo eShop Project
======================================

Functionality
-------------
    * Create a new category eshop_category for products;
    * Add fields on product.product:
        * 'eShop Category': category in the eShop;
        * 'Min date' and 'Max Date' that make product available for sale;
    * Add fields on res.partner:
        * 'Can purchase on eShop';
        * 'eShop password';

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
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
        'demo/eshop_category.yml',
        'demo/product_product.yml',
        'demo/product_uom.yml',
        'demo/function.xml',
        'demo/res_users.yml',
        'demo/res_groups.yml',
    ],
    'installable': False,
}
