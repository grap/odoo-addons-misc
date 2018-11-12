.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================
Users Partners Access
=====================


In Odoo, a user has a partner associated. This feature is great to manage
commun fields, but generate some non desired behaviours in some multi company
cases:

If a user has multi company access, the company of the associated partner will
change when the user change company. So the associated partner will be
"available or not", depending of user configuration. This generates error
access.

With this module:

* the users partners will be disabled. This will force saler / purchaser
  to create new partner (if the user is a customer or a supplier too)
* the users partners will have no company, this will fix all bug access;


Technically
-----------

All partners associated to a user:

* have ``active``, ``customer``, ``supplier`` checkbox disabled;
* have ``company_id`` empty;

Only members of 'Administration / Access Rights' could update partners;

Credits
=======

Contributors
------------

* Sylvain Legal, GRAP <sylvain.legal@grap.coop> (http://www.grap.coop/)
* Quentin Dupont, GRAP <quentin.dupont@grap.coop> (http://www.grap.coop/)

Do not contact contributors directly about support or help with technical issues.

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
