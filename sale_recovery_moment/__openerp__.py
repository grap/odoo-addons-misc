# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
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
    'name': 'Sale - Recovery Moment',
    'version': '0.2',
    'summary': """Manage Recovery Moments and Places for Sale Order""",
    'category': 'Sale',
    'description': """
Manage Recovery Moments and Places for Sale Order
=================================================

Functionality:
--------------
    * Add Recovery Moment Group that is a group of Recovery Moment;
    * A recovery Moment is a moment during the customers have the possibility
      to recover them sales; A recovery moment is described by:
        * A min date and a max date;
        * A place (sale.recovery.place);
    * Add Product.prepare.category Model that is a new type of product:
        * The picking created can be reordered by Prepare Category
          (with a wizard);

Technical Information:
----------------------
    * Possibility to create a cron task to send email to customers, to remind
      them to recover their Orders.
      The cron task must be set with:
        * model: 'sale.order';
        * function:  _send_reminder_email;
        * args: ([company_ids], hours)

Technical Limits:
-----------------
    * This module displays some Total of Sale Orders; This amount will be wrong
    in a multicurrencies context for the instance;

Copyright, Authors and Licence:
-------------------------------
    * Copyright: 2014, GRAP: Groupement Régional Alimentaire de Proximité;
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale_stock',
        'report_webkit',
        'sale_order_dates',
        'sale_visible_tax',
        'stock_picking_reorder_lines',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir_module_category.yml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'data/ir_sequence_type.yml',
        'data/ir_sequence.yml',
        'view/view_related.xml',
        'view/action_related.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/sale_recovery_place.yml',
        'demo/sale_recovery_moment_group.yml',
        'demo/sale_recovery_moment.yml',
        'demo/sale_delivery_category.yml',
        'demo/product_delivery_category.yml',
        'demo/res_partner.yml',
        'demo/sale_order.yml',
        'demo/res_groups.yml',
    ],
    'css': [
        'static/src/css/css.css',
    ],
    'images': [
    ],
    'installable': False,
}
