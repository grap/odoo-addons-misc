# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import TransientModel
from openerp.osv import fields
import openerp.addons.decimal_precision as dp


class StockPickingMassChangeWizardLine(TransientModel):
    _name = 'stock.picking.mass.change.wizard.line'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'stock.picking.mass.change.wizard', 'Wizard', select=True),
        'picking_id': fields.many2one(
            'stock.picking', 'Picking', required=True, readonly=True),
        'move_id': fields.many2one(
            'stock.move', 'Picking', required=True, readonly=True),
        'sale_id': fields.many2one(
            'sale.order', 'Sale Order', readonly=True),
        'ordered_qty': fields.float(
            'Ordered Qty', required=True, readonly=True,
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'exact_target_qty': fields.float(
            'Theoretical Target Qty', required=True, readonly=True,
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'target_qty': fields.float(
            'Target Qty', required=True,
            digits_compute=dp.get_precision('Product Unit of Measure')),
        'partner_id': fields.many2one(
            'res.partner', 'Partner', required=True, readonly=True),
    }
