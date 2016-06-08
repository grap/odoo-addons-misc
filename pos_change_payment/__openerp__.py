# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Point Of Sale - Change Payment',
    'summary': """Improve payment changes when user did a mistake and"""
            """ disable some actions on POS Bank Statement Line""",
    'version': '0.2',
    'category': 'Point Of Sale',
    'description': """
Improve payment changes when user did a mistake and disable some actions on POS
 Bank Statement Line
===============================================================================
====================

Functionality:
--------------
    * Add the possibility to switch a POS payment (account.bank.statement.line)
      of a POS Order from a Journal to another. This feature is usefull when
      the user realized that he did a mistake, during the close of the session,
      or just after he marked the POS as paid;
      (Only if entries has not been generated)
    * Add the possibility to change all payments (method and amount) of a POS;
      (Only if entries has not been generated)

Bug Fixes / Improvement:
------------------------
    * In the pos.payment wizard, display only the payment methods defined in
      the current POS session;
    * Disable the possibility to edit / delete a bank statement line on a POS
      Order that has generated his entries, except using the wizard of this
      module. This will prevent the generation of bad account move during
      the close of the session; (mainly unbalanced moves)
    * All the cash payment are merged into a single one statement line. this
      feature is usefull if the user use OpenERP as a calculator, writing
      for a payment:
        * Payment 1/ Cash 50 €;
        * Payment 2/ Cash -3,56 €;
        * With this module, the final statement line is a single line
          Payment 1/ Cash 46,44 €


Copyright, Authors and Licence:
-------------------------------
    * Copyright:
        * 2013-Today, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/action.xml',
        'views/view.xml',
        'views/view_pos_switch_journal_wizard.xml',
    ],
    'installable': True,
}
