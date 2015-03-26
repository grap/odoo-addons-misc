# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Easy Valuation for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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


class stock_easy_valuation_wizard_category_line(TransientModel):
    _name = 'stock.easy.valuation.wizard.category.line'
    _rec_name = 'category_id'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'stock.easy.valuation.wizard',
            'Wizard', select=True),
        'category_id': fields.many2one(
            'product.category', 'Category', readonly=True),
        'product_line_ids': fields.one2many(
            'stock.easy.valuation.wizard.product.line', 'category_line_id',
            'Products', readonly=True),
        'valuation': fields.float(
            'Valuation', readonly=True),
    }
