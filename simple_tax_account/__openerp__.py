# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account - Simple Tax',
    'summary': 'Easy Switch between VAT Excluded and VAT Included',
    'version': '8.0.1.0.0',
    'category': 'Account',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/view_res_partner.xml',
        'views/view_account_invoice.xml',
        'views/view_account_tax.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/account_tax.yml',
        'demo/res_partner.yml',
        'demo/product_product.yml',
    ],
    'installable': True,
}
