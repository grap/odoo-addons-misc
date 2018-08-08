.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===========================
Stock Picking - Mass Change
===========================

This module extends Odoo Stock module to provide a wizard to easily mass edit
pickings.

It provides a wizard where user can select a product, and some method to change
product quantities massively, if the user doesn't have enough product to give
to its customers.

2 methods are implemented

* A prorata method, the wizard will redistribute fairly, reducing the quantity
  for all the moves.

.. figure:: /stock_picking_mass_change/static/description/wizard_form_pro_rata.png
   :width: 800 px

* A fifo method, the wizard will reduce the quantity of the last pickings.

.. figure:: /stock_picking_mass_change/static/description/wizard_form_fifo.png
   :width: 800 px


Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
