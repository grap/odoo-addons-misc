# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale - eShop',
    'version': '8.0.4.0.0',
    'summary': "Allow connection to Odoo eShop Project",
    'category': 'Sale',
    'author': 'GRAP',
    'license': 'AGPL-3',
    'depends': [
        'mail',
        'product',
        'sale',
        'sale_food',
        'sale_order_line_price_subtotal_gross',
        'sale_recovery_moment',
        'simple_tax_sale',
        'grap_qweb_report',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'data/ir_cron.xml',
        'views/menu.xml',
        'views/view_account_tax.xml',
        'views/view_eshop_category.xml',
        'views/view_product_product.xml',
        'views/view_product_uom.xml',
        'views/view_res_company.xml',
        'views/view_res_partner.xml',
        'views/view_wizard_res_company_eshop_setting.xml',
    ],
    'demo': [
        'demo/res_company.xml',
        'demo/eshop_category.xml',
        'demo/product_product.xml',
        'demo/product_uom.xml',
        'demo/res_users.xml',
        'demo/res_groups.xml',
        'demo/res_partner.xml',
    ],
    'installable': True,
}
