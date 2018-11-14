# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale - eShop',
    'version': '8.0.2.0.0',
    'summary': "Allow connection to Odoo eShop Project",
    'category': 'Sale',
    'author': 'GRAP',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'mail',
        'sale',
        'sale_recovery_moment',
        'simple_tax_sale',
        'sale_food',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'views/menu.xml',
        'views/view_account_tax.xml',
        'views/view_eshop_category.xml',
        'views/view_product_product.xml',
        'views/view_product_uom.xml',
        'views/view_res_company.xml',
        'views/view_res_partner.xml',
    ],
    'demo': [
        'demo/res_partner.xml',
        'demo/eshop_category.xml',
        'demo/product_product.xml',
        'demo/product_uom.xml',
        'demo/res_users.xml',
        'demo/res_groups.xml',
    ],
    'installable': True,
}
