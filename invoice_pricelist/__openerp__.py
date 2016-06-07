# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Invoice Price List',
    'version': '1.0',
    'category': 'account',
    'description': """
Add Pricelist feature on invoices
=================================

Functionnality
--------------
* Add pricelist field on account invoices. This field is now required

* Add price computation on each account invoice line based on pricelist

* Possibility to group by pricelist on account.invoice view

Technical points
----------------

As this field is not in the core, this module will:
* populate existing invoices with default partner pricelist;
* overload create function to add default partner pricelist if not set;

Odoo core is bad designed for partner pricelist:
* the sale pricelist (property_product_pricelist) is in the product module
* the purchase pricelist (property_product_pricelist_purchase is in the
  purchase module
So, as both field are necessary to compute pricelist, this module requires
'purchase' module installation.

In the same way, to make price computation consistent with sale and purchase
modules, this module only call onchange function of sale and purchase module
and provides same values. So 'sale' and 'purchase' module are required.

Roadmap / Issue
---------------
Invoices created via picking created via purchase / sale order will inherit
pricelist from sale or purchase order, but invoices created directly via
purchase or sale will have default partner pricelist.

Please make Pull request with functions that overload invoice prepare functions
in sale and purchase module.


Copyright, Author and Licence
-----------------------------

* Copyright: 2015, Groupement Régional Alimentaire de Proximité
* Author: Sylvain LE GAL (https://twitter.com/legalsylvain)
* Licence: AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'sale',
        'purchase',
        'stock',
    ],
    'data': [
        'views/view_account_invoice.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_pricelist.yml',
        'demo/res_partner.yml',
    ],
    'installable': False,
}
