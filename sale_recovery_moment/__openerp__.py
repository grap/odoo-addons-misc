# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale - Recovery Moments',
    'version': '8.0.1.0.0',
    'summary': "Manage Recovery Moments and Places for Sale Order",
    'category': 'Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'stock',
        'report_webkit',
        'sale_order_dates',
        'stock_picking_reorder_lines',
        'web_widget_color',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_type.xml',
        'data/ir_sequence.xml',
        'views/view_related.xml',
        'views/action_related.xml',
        'views/view_product_prepare_category.xml',
        'views/view_product_product.xml',
        'views/view_res_company.xml',
        'views/view_sale_order.xml',
        'views/view_sale_recovery_moment.xml',
        'views/view_sale_recovery_moment_group.xml',
        'views/view_sale_recovery_moment_group_wizard_duplicate.xml',
        'views/view_sale_recovery_place.xml',
        'views/view_stock_move.xml',
        'views/view_stock_picking.xml',
#        'views/view_stock_picking_reorder.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    'demo': [
        'demo/sale_recovery_place.xml',
        'demo/sale_recovery_moment_group.xml',
        'demo/sale_recovery_moment.xml',
        'demo/product_prepare_category.xml',
        'demo/sale_order.xml',
        'demo/res_groups.xml',
    ],

    'installable': True,
}
