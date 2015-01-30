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
from openerp.osv import fields


class sale_recovery_moment_group_wizard_product_list_line(TransientModel):
    _name = 'sale.recovery.moment.group.wizard.product.list.line'
    _rec_name = 'product_id'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'sale.recovery.moment.group.wizard.product.list',
            'Wizard', select=True),
        'product_id': fields.many2one(
            'product.product', 'Product', readonly=True),
        'confirmed_qty': fields.float('Confirmed Quantity', readonly=True),
        'qty_available': fields.float('Quantity On Hand', readonly=True),
        'incoming_qty': fields.float('Incoming Quantity', readonly=True),
        'outgoing_qty': fields.float('Outgoing Quantity', readonly=True),
    }

    # Defaults Section
    _defaults = {
    }
