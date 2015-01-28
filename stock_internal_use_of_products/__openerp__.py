# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Internal Use Of Products for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
    'name': 'Stock Internal Use of products ',
    'version': '1.0',
    'category': 'Stock',
    'description': """
Allow non accountant user to declare the use of stockable products for
specific uses (eg: gifts, tastings, etc.)
======================================================================
=========================================

Features:
---------
    * add a 'Internal Use' menu to register such uses
    * add a 'Internal Use Line' menu mostly for reporting purposes

Technical informations :
------------------------
    * add a 'Internal Use Case' menu to configure the internal use
    possibilities
    * for each internal_use_case, you need to define an inventory-type
    stock_location

    * Confirming an internal_use will create
        * 1 stock.picking
        * 1 stock.move for each internal_use.line between the 2 locations
        defined in the internal_use_case
        * (1 account.move if your products are defined in real_time inventory)
        * 1 account.move to transfer the expense

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Julien WESTE;""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'product',
        'stock',
    ],
    'data': [
        'data/ir_sequence.xml',
        'security/ir_model_access_data.yml',
        'security/ir_rule_data.yml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/stock_location.yml',
        'demo/res_groups.yml',
        'demo/internal_use_case.yml',
        'demo/internal_use.yml',
    ],
    'css': [
        'static/src/css/css.css'
    ],
}
