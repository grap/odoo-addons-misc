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
    _rec_name = 'offset'

    _FORMAT_SELECTION = [
        ('normal', 'Normal'),
        ('tall', 'Tall'),
    ]

    def _needaction_count(self, cr, uid, domain=None, context=None):
        pp_obj = self.pool['product.product']
        pp_ids = pp_obj.search(cr, uid, [
            ('pricetag_state', 'in', ('1', '2'))], context=context)
        return len(pp_ids)

    def initialize_product(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids[0], context=context)
        ctx = context.copy()
        ctx['format'] = wizard.format
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
        if context.get('active_id', False):
            pp_obj = self.pool['product.product']
            custom_format = context.get('format', 'normal')
            if custom_format == 'normal':
                limit = 14
            elif custom_format == 'tall':
                limit = 8
            else:
                limit = 1
            pp_ids = pp_obj.search(cr, uid, [
                ('pricetag_state', 'in', ['1', '2'])],
                order='pricetag_state desc',
                limit=limit,
            )
            for pp_id in pp_ids:
                res.append((0, 0, {
                    'product_id': pp_id,
                    'quantity': 1,
                    'print_unit_price': True,
                }))
        return res

    # Fields Default Section
    def _get_format(self, cr, uid, context=None):
        return context.get('format', 'normal')

    # Columns Section
    _columns = {
        'offset': fields.integer(
            'Offset', required=True, help="Price Tag number not to print"),
        'border': fields.boolean(
            'Border', help="Design a border on Price Tags"),
        'radar_chart': fields.boolean(
            'Radar Chart', help="Display Radar Chart if available"),
        'line_ids': fields.one2many(
            'product.pricetag.wizard.line', 'wizard_id', 'Products'),
        'format': fields.selection(
            selection=_FORMAT_SELECTION, string='format'),
    }

    # Default values Section
    _defaults = {
        'border': True,
        'radar_chart': True,
        'offset': 0,
        'line_ids': _get_line_ids,
        'format': _get_format,
    }
