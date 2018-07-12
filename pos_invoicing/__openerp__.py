# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Point Of Sale - Invoicing',
    'summary': 'Handle invoicing from Point Of Sale',
    'version': '2.1',
    'category': 'Point of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'account_voucher',
        'point_of_sale',
    ],
    'data': [
        'view/pos_invoice_draft_order_wizard_view.xml',
        'view/action.xml',
        'view/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'installable': True,
}
