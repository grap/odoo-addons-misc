# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Print Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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
