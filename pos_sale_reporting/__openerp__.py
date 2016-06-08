# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale / Point Of Sale Report module for OpenERP
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
    'name': 'Point Of Sale & Sale Reporting',
    'summary': 'Add reports merging sale and point of sale informations',
    'version': '0.2',
    'category': 'Point Of Sale',
    'description': """
Add reports merging sale and point of sale informations
=======================================================

Functionality:
--------------
    * Add a graph report view in the Report menu to merge sale and point
      of sale Net informations;
        * Net Sales Evolution;
        * Net Sales by Category (3 levels);
        * Top Products saled;

Technical Information:
----------------------
    * As this module merge point of sale and sale information, the sql views
      are using UNION statement; So, performance are very bad, and to avoid
      that this module create MATERIALIZED view;
    * So information doesn't take into account, last day sales;
    * A cron Task update the materialized view each night;

Specific Version:
-----------------
    * you so need Postgresql 9.3+ to install this module;

Ref:
----
http://stackoverflow.com/questions/18134798/why-does-my-view-in-postgresql"""
    """-not-use-the-index

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'point_of_sale',
        'invoice_pricelist',
    ],
    'data': [
        'data/ir_cron.xml',
        'security/ir_model_access.yml',
        'security/ir_rule.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'images': [
        'static/src/img/screenshots/1.png'
    ],
    'installable': True,
}
