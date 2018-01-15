# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Change Payment module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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
    'name': 'Point Of Sale - Payments Change',
    'version': '8.0.1.0.0',
    'category': 'Point Of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/action.xml',
        'views/view_account_bank_statement.xml',
        'views/view_pos_change_payments_wizard.xml',
        'views/view_pos_order.xml',
        'views/view_pos_switch_journal_wizard.xml',
    ],
    'installable': True,
}
