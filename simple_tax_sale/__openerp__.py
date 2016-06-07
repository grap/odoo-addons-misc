# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Simple Tax module for Odoo
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
    'name': 'Sale - Simple Tax',
    'summary': 'Easy Switch between VAT Excluded and VAT Included For Sale',
    'version': '0.1',
    'category': 'Sale',
    'description': """
Easy Switch between VAT Excluded and VAT Included For Sale Module
=================================================================

Feature:
--------
* Possibility to switch between Price VAT Included and Price VAT Excluded
  when editing a Sale Order;

See simple_tax_account for more information

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
        'simple_tax_account',
        'sale',
    ],
    'data': [
        'view/view.xml',
    ],
    'auto_install': True,
    'installable': False,
}
