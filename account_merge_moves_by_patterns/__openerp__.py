# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Merge Moves By Patterns for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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
    'name': 'Account - Merge moves by Patterns',
    'version': '0.2',
    'category': 'Account',
    'description': """
Add possibility to merge account moves
======================================

Features :
----------
    * Add a feature to merge a lot of account moves that have the same patterns
    * A Pattern is defined by:
        * a company;
        * a list of credit accounts, a list of debit account ;
        * a Period;
    * The 'Merged' move will be at 'draft' state during all the period,
      and will be validated at the end of the period;
    * Possibility to batch the merge process;

Use Case :
----------
    * This module can be used for exemple if OpenERP is set to generated
      account moves at each stock moves in real time;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'installable': False,
}
