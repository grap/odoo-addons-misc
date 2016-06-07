# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Easy Valuation for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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
    'name': 'Stock - Easy Valuation',
    'version': '2.0',
    'category': 'Stock',
    'description': """
Add Extra Tools to valuate stock
================================

Pending valuation:
------------------
    * Add an extra menu item in 'stock' to have the valuation of all active
      product instantly;

Valuation at any date:
----------------------
    * Add an extra wizard to have the valuation of the stock for all product.
      This feature is very usefull for accounting people that need to have the
      valuation of the stock at the last day of the accounting year.
      The wizard realize a document with the list of all product.
        * Select products filtered by category_ids;
        * Select values filtered by warehouse_id;
        * Possibility to include changes of inventories realized after the
          requested date. (Usefull if we want the valuation of the stock at
          31/12/2014 but the inventory appended 15/01/2015.

Limits / Known Issues:
----------------------
    * Doesn't manage multicurrency. the currency used is the currency of the
      Current Company;

Copyright, Authors and Licence:
-------------------------------
    * Copyright:
        * 2014-Today, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'report/stock_easy_valuation_report.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'installable': False,
}
