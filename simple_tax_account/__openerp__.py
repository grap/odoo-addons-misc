# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Simple Tax module for Odoo
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
    'name': 'Account - Simple Tax',
    'summary': 'Easy Switch between VAT Excluded and VAT Included',
    'version': '0.1',
    'category': 'Account',
    'description': """
Easy Switch between VAT Excluded and VAT Included
=================================================

Use case:
---------
This module is useful in the following case:
* Odoo is implemented in a country with simple Taxes system, (Like in France)
  with generaly only one Tax type='percent'. (VAT)
* Users define allways product price with VAT included. (or allways excluded);
* Some customers / suppliers wants quotation / invoices with the other system;

Feature:
--------
* On account.tax, add a new field 'simple_tax_id' that is the according VAT
  with or without TAX included. Sample:
      * TAX A: VAT 10% included;
      * TAX B : VAT 10% excluded;
      * TAX A and TAX B will be linked together;
* On res.partner, add a new field selection 'simple_tax_type' with
  the following values:
    * 'none' : (default) undefined, the Tax will be the tax of the product;
    * 'excluded': All price will be recomputed with Tax excluded;
    * 'included': All price will be recomputed with Tax inluded;
* Possibility to switch between Price VAT Included and Price VAT Excluded
  when editing a Account Invoice;

Related Modules:
----------------
* This following modules provide the same behouviour:
    * 'simple_tax_sale' for sale module;
    * 'simple_tax_purchase' for purchase module;

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
        'account',
    ],
    'data': [
        'view/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/account_tax.yml',
        'demo/res_partner.yml',
        'demo/product_product.yml',
    ],
    'installable': False,
}
