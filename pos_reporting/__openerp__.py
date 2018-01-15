# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale - Reporting for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
    'name': 'Point of Sale Reporting',
    'version': '3.0',
    'category': 'Point of Sale',
    'description': """
Adds dashboard showing the sales with a bar graph
=================================================

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
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
        'view/view.xml',
        'view/action.xml',
        'view/view2.xml',
        'view/action2.xml',
        'view/menu.xml',
        'security/ir_model_access.yml',
        'security/ir_rule.xml',
    ],
    'installable': True,
}
