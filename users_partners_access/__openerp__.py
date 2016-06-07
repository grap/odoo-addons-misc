# -*- encoding: utf-8 -*-
##############################################################################
#
#    User Partners Access module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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
    'name': 'Users Partners access',
    'summary': 'Users Partners Access',
    'version': '2.1',
    'category': 'base',
    'description': """
Users Partners Access
=====================

In Odoo, a user has a partner associated. This feature is great to manage
commun fields, but generate some non desired behaviours in some multi company
cases:

If a user has multi company access, the company of the associated partner will
change when the user change company. So the associated partner will be
"available or not", depending of user configuration. This generates error
access.

With this module:
    * the users partners will be disabled. This will force saler / purchaser
      to create new partner (if the user is a customer or a supplier too)
    * the users partners will have no company, this will fix all bug access;


Technically:
------------
    * all partners associated to a user:
        * have 'active', 'customer', 'supplier' checkbox disabled;
        * have 'company_id' empty;
    * Only members of 'Administration / Access Rights' could update partners;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2015-Today GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'data/function.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'installable': False,
}
