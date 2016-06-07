.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Add Pricelist feature on invoices
=================================

* Add pricelist field on account invoices. This field is now required
* Add price computation on each account invoice line based on pricelist
* Possibility to group by pricelist on account.invoice view

.. image:: /invoice_pricelist/static/description/invoice_with_pricelist.png

Technical points
================

As this field is not in the core, this module will:

* populate existing invoices with default partner pricelist;
* overload create function to add default partner pricelist if not set;

Odoo core is bad designed for partner pricelist:

* the sale pricelist (property_product_pricelist) is in the 'product' module
* the 'purchase' pricelist (property_product_pricelist_purchase is in the
  purchase module

So, as both field are necessary to compute pricelist, this module requires
'purchase' module installation.

In the same way, to make price computation consistent with sale and purchase
modules, this module only call onchange function of sale and purchase module
and provides same values. So 'sale' and 'purchase' module are required.

Roadmap / Issue
===============

Invoices created via picking created via purchase / sale order will inherit
pricelist from sale or purchase order, but invoices created directly via
purchase or sale will have default partner pricelist.

Please make Pull request with functions that overload invoice prepare functions
in sale and purchase module.

Installation
============

Normal installation.

Configuration
=============

No configuration is needed.

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>
