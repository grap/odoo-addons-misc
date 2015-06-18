# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
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


class StockPickingReorder(TransientModel):
    _name = 'stock.picking.reorder'
    _description = 'Stock Picking Reorder Moves'

    def reorder(self, cr, uid, ids, context=None):
        context = context or {}
        picking_obj = self.pool['stock.picking']
        picking_ids = context.get('active_ids')
        picking_obj.reorder_moves_by_category_and_name(
            cr, uid, picking_ids, context=context)
        return True
