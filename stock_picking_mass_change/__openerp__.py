# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock Picking - Mass Change',
    'summary': 'Possibility to change massively a product for many pickings',
    'version': '8.0.2.0.0',
    'category': 'Stock',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/view_stock_picking_mass_change_wizard.xml',
    ],
    'demo': [
        'demo/stock_picking.xml',
        'demo/stock_move.xml',
    ],
    'images': [
        '/static/description/wizard_form_fifo.png',
        '/static/description/wizard_form_pro_rata.png',
    ],
    'installable': True,
}
