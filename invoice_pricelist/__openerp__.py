# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Invoice Price List',
    'version': '1.0',
    'category': 'account',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'sale',
        'purchase',
        'stock',
    ],
    'data': [
        'views/view_account_invoice.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_pricelist.yml',
        'demo/res_partner.yml',
    ],
    'installable': True,
}
