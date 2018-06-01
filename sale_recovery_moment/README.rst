.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
Sale - Recovery Moments
=======================

This module extends the functionality of sale module to provide extra models
to handle sales with organized by the saler in a calendar.


Functionality
-------------

* A ```sale.recovery.place``` is a place where the customer can recover his
  order.

.. figure:: /sale_recovery_moment/static/description/sale_recovery_place_tree.png
   :width: 800 px

* A ```sale.recovery.moment``` is a moment during the customers have the
  possibility to recover their sales; A recovery moment is described by a min
  date and a max date for the recovery and a place where the sale orders is
  available.

.. figure:: /sale_recovery_moment/static/description/sale_recovery_moment_calendar.png
   :width: 800 px

* A ```sale.recovery.moment.group``` is a group of Recovery Moments with a
  start date and a end date of sale.

.. figure:: /sale_recovery_moment/static/description/sale_recovery_moment_group_form.png
   :width: 800 px


* A ```product.prepare.category```  is a new category of product

.. figure:: /sale_recovery_moment/static/description/sale_prepare_category_tree.png
   :width: 800 px

The picking created can be reordered by Prepare Categories with a wizard.

Technical Limits
----------------

* This module displays some Total of Sale Orders; This amount will be wrong
in a multicurrencies context for the instance;


Credits
=======

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
