# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Product - EAN Duplicates',
    'summary': 'Detect and fix easily EAN duplicates',
    'version': '8.0.1.0.0',
    'category': 'product',
    'description': """
Detect and fix easily EAN duplicates
====================================

Functionality:
--------------
    * Add a view to detect and fix EAN duplicates of products into a company;
    * Remove in the copy fields of product product the field ean;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
    ],
    'data': [
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
}
