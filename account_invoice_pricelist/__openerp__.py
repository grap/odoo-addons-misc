# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Price List on Invoice for Odoo
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
    'name': 'Account - Price List on Invoice',
    'version': '1.0',
    'category': 'account',
    'description': """
Simply add the pricelist of the partner on invoices
===================================================

Functionnality:
---------------
    * Add a stored field pricelist on invoices, related to partner;
    * Possibility to group by pricelist on account.invoice view;

Limitation:
-----------
    * The computation of the price is not set;
    * The field will not be stored for purchase pricelist as long as 'purchase'
      module is not installed; (in invoice / in refund)

This module is usefull to do reporting.

Copyright, Author and Licence:
------------------------------
    * Copyright: 2015, Groupement Régional Alimentaire de Proximité
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    * Licence: AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'view/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'installable': False,
}
