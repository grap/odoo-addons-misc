# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class StockPicking(Model):
    _inherit = 'stock.picking'

    def button_quick_edit_wizard(self, cr, uid, ids, context=None):
        context.update({
            'active_model': self._name,
            'active_ids': ids,
            'active_id': len(ids) and ids[0] or False
        })
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking.quick.edit.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'nodestroy': True,
        }
