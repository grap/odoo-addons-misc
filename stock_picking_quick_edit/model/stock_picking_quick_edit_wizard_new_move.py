# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Picking Quick Edit module for Odoo
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

from openerp.osv import orm, fields


class StockPickingQuickEditWizardNewMove(orm.TransientModel):
    _name = 'stock.picking.quick.edit.wizard.new.move'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'stock.picking.quick.edit.wizard', 'Wizard',
            select=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True),
        'product_qty': fields.float(
            'Quantity', required=True),
        'product_uom': fields.many2one(
            'product.uom', 'UoM', readonly=True),
    }

    # View Section
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        pp_obj = self.pool['product.product']
        if not product_id:
            return {
                'product_qty': 0,
                'product_uom': False,
            }
        pp = pp_obj.browse(cr, uid, product_id, context=context)
        return {'value': {
            'product_uom': pp.uom_id.id,
            'product_qty': 1.00,
        }}
