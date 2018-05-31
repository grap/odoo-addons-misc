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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import fields
from openerp.osv.orm import Model


class stock_move(Model):
    _inherit = 'stock.move'

    # Column Section
    _columns = {
        'prepare_categ_id': fields.related(
            'product_id', 'prepare_categ_id', type='many2one',
            relation='product.prepare.category', store=True,
            string='Prepare Category', readonly=True),
    }

    def _prepare_picking_assign(self, cr, uid, move, context=None):
        res = super(stock_move, self)._prepare_picking_assign(
            cr, uid, move, context=context)
        res.update({
            'recovery_moment_id':
            move.procurement_id.group_id.recovery_moment_id.id,
            'delivery_moment_id':
            move.procurement_id.group_id.delivery_moment_id.id,
        })
        return res
