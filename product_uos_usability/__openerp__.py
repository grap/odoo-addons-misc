# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - UoS usability module for Odoo
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
    'name': 'Product - UoS usability',
    'summary': 'Apply Specific behaviour for Unit of Sale',
    'version': '1.0',
    'category': 'Sale',
    'description': """
Apply Specific behaviour for Unit of Sale
=========================================

Feature
-------

We could name this module the 'Sausage' module.
It makes more easy to sell sausages in Odoo.

Basically, with the following example:
* We have a sausage of 0.350 kg;
* We sell piece of sausage to customers (Unit);
* We make stock inventory weighing sausages (kg);
* Weh invoice exactely what we delivered (kg);

So with Odoo Core, we set in product template:
* uom_id: kg;
* uos_id: Unit;
* list_price: 28€ (ie. 28€ / kg);

This module
* In Product Form View:
    * add a new field 'uos_coeff_inv' that is the inverse concept of existing
      'uos_coeff' field. In the sample, we'll set:
        * 'uos_coeff_inv': 0.350 kg. Odoo will compute 2.857 for 'uos_coeff';

* In product Tree View:
    * create a new editable tree view to edit more quickly 'uos_coeff_inv' and
      'uos_id' fields;

* In Sale Order Form:
    * add 'product_uos' in the main view, as readonly field;
    * add 'product_uos_qty' in the main view, if 'product_uos' is defined;
    * Without this module, change 'product_qty' (0.350 kg) change
      'product_uos_qty' (1 Unit).
        * This module add the reverse behaviour.

* In the Delivery Form:
    * Without this module, change 'product_qty' (0.350 kg) changes
      'product_uos_qty' (1 Unit);
        * This module **disables** that feature;
    * Without this module, change 'product_uos_qty' (1 Unit) changes
      'product_qty' (0.350 kg);
        * This module keeps that feature;

    * Consequently, We can finally deliver one sausage with the following
      information:
        * 'product_uos_qty': 1 Unit. (Real Delivered Quantity);
        * 'product_qty': 0.324 kg. (Real Delivery Weight);

    * While, invoicing this will generate an Invoice with the uom_id of the
      product, instead of the uos_id.
        * **This module so fixes a bug (V7.0)**, because for the time being,
          the module generates a line with:
            * quantity: 1  Unit;
            * price_unit: 28 €; 
            * Total: 28 €, which is incorrect and rather expensive for a
              sausage !
        * With this module, the generated invoice line has this info:
            * quantity: 0.324 kg;
            * price_unit: 28 €;
            * Total: 9.07 €, which is still cheaper !
              (even if the meat is expensive, and that is a good reason to
              consume less, or to become a vegetarian.)

Technical information
---------------------

* Overload 

* Add a not null constraint on existing field 'uos_coeff';

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
        'sale',
        'stock',
    ],
    'data': [
        'views/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_product.yml',
    ],
}
