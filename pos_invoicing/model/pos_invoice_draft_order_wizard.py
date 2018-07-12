# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import TransientModel


class PosInvoiceDraftOrderWizard(TransientModel):
    _name = 'pos.invoice.draft.order.wizard'

    # Action section
    def invoice_draft_order(self, cr, uid, ids, context=None):
        order_id = context.get('active_id', False)
        if not order_id or context.get('active_model', False) != 'pos.order':
            return False
        po_obj = self.pool.get('pos.order')
        res = po_obj.action_invoice(cr, uid, [order_id], context=context)
        return res
