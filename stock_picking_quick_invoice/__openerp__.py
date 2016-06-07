# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Picking Quick Edit module for Odoo
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
    'name': 'Stock - Picking Quick Invoice',
    'summary': 'Possibility to invoice a Delivery Order',
    'version': '0.1',
    'category': 'Stock',
    'description': """
Possibility to Invoice and mark payment for a Delivery Order
============================================================

Functionality:
--------------

* Provide a wizard to invoice a pending Picking:
    * display amount;
    * display payments line;


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
        'account_voucher',
    ],
    'data': [
        'views/view_account_journal.xml',
        'views/view_stock_picking.xml',
        'views/view_stock_picking_quick_invoice_wizard.xml',
    ],
    'installable': False,
}
