# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Food Module for Odoo
#    Copyright (C) 2012-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
from openerp.tools.translate import _


class product_pricetag_wizard(TransientModel):
    _name = 'product.pricetag.wizard'
    _inherit = 'ir.needaction_mixin'
    _rec_name = 'border'

    _FORMAT_SELECTION = [
        ('small', 'Small (Epicerie des Halles)'),
        ('normal', 'Normal (GRAP)'),
        ('tall', 'Tall (Vrac En Vert)'),
    ]

    def _needaction_count(self, cr, uid, domain=None, context=None):
        pp_obj = self.pool['product.product']
        pp_ids = pp_obj.search(cr, uid, [
            ('pricetag_state', 'in', ('1', '2'))], context=context)
        return len(pp_ids)

    def initialize_product(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)
        product_obj = self.pool['product.product']
        product_ids = product_obj.search(cr, uid, [
            ('pricetag_state', 'in', ['1', '2'])],
            order='pricetag_state desc', limit=wizard.limit)
        ctx = context.copy()
        ctx.update({
            'active_model': 'product.product',
            'active_ids': product_ids,
            'border': wizard.border,
            'radar_chart': wizard.radar_chart,
            'format': wizard.format,
            'limit': wizard.limit,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': _('Print Price Tags'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'product.pricetag.wizard',
            'res_id': None,
            'target': 'new',
            'context': ctx,
        }

    # Fields Default Section
    def _get_line_ids(self, cr, uid, context=None):
        res = []
        context = context and context or {}
        if context.get('active_model', False) == 'product.product':
            product_ids = context.get('active_ids', [])
            for product_id in product_ids:
                res.append((0, 0, {
                    'product_id': product_id,
                    'quantity': 1,
                }))
        return res

    def _get_border(self, cr, uid, context=None):
        return context.get('border', True)

    def _get_radar_chart(self, cr, uid, context=None):
        return context.get('radar_chart', True)

    def _get_format(self, cr, uid, context=None):
        return context.get('format', 'normal')

    def _get_limit(self, cr, uid, context=None):
        return context.get('limit', 10000)

    # Columns Section
    _columns = {
        'border': fields.boolean(
            'Border', help="Design a border on Price Tags"),
        'limit': fields.integer('Initialization Limit', required=True),
        'radar_chart': fields.boolean(
            'Radar Chart', help="Display Radar Chart if available"),
        'line_ids': fields.one2many(
            'product.pricetag.wizard.line', 'wizard_id', 'Products'),
        'format': fields.selection(
            selection=_FORMAT_SELECTION, string='format', required=True),
    }

    # Default values Section
    _defaults = {
        'border': _get_border,
        'radar_chart': _get_radar_chart,
        'format': _get_format,
        'limit': _get_limit,
        'line_ids': _get_line_ids,
    }
