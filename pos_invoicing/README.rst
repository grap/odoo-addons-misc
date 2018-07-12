.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=========================
Point Of Sale - Invoicing
=========================

Feature Case 1: (Fix Odoo Behaviour)
------------------------------------

When you pay a pos_order, and then create an invoice :

* you mustn't register a payment against the invoice as the payment
  already exists in POS;
* The POS payment will be reconciled with the invoice when the session
  is closed.
* You mustn't modify the invoice because the amount could become
  different from the one registered in POS. Thus we have to
  automatically validate the created invoice.

Feature Case 2: (New feature)
-----------------------------

If you want to give an invoice to your POS customer and let him pay
latter:

* you have to validate the pos_order without payments and to create
  an invoice to receive the payments.

Functionality
-------------
About the invoices created from POS after payment:
* automatically validate them and don't allow modifications;
* remove the Pay button;
* Don't display them in the Customer Payment tool;

About the invoices created from POS before payment:
* possibility to create a draft invoice from a draft pos_order;

Technically
-----------

add a forbid_payment flag on account_invoice to mark the items that
shouldn't be paid.

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
