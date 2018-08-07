# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Picking - Quick Edit',
    'summary': 'Possibility to quickly edit a stock picking',
    'version': '8.0.1.0.0',
    'category': 'Stock',
    'description': """
Possibility to edit a Delivery Order
====================================

Functionality:
--------------
    * Provide a wizard to edit a pending Picking:
        * Add some product;
        * Change quantity;
        * Remove lines. (set to 0 the quantity);


Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2015, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/view_stock_picking_quick_edit_wizard.xml',
        'views/view_stock_picking.xml',
    ],
    'installable': True,
}
