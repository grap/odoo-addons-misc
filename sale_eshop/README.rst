.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Allow connection to Odoo eShop Project
======================================

This module is the 'odoo' part of the project Odoo eShop.

the 'client' part is available here : https://github.com/grap/odoo-eshop

eShop Categories
----------------

Add a new model ``eshop.category`` to have the possibility to dispatch products
for the eshop.


* Create a new category eshop_category for products
* Add fields on product.product
    * 'eShop Category': category in the eShop
    * 'Min date' and 'Max Date' that make product available for sale
* Add fields on res.partner
    * 'Can purchase on eShop'
    * 'eShop password'

.. figure:: /pos_multicompany/static/description/pos_category_tree.png
   :width: 800 px

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
