# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv
from openerp.osv.orm import Model
from openerp.tools.translate import _
from openerp import netsvc


class PosOrder(Model):
    _inherit = 'pos.order'

    def action_invoice(self, cr, uid, ids, context=None):
        inv_obj = self.pool['account.invoice']
        wf_service = netsvc.LocalService('workflow')
        for po in self.browse(cr, uid, ids, context=context):
            if po.state not in ('draft', 'paid'):
                raise osv.except_osv(
                    _('Error!'),
                    _("You can not invoice a non new or non paid POS Order"))
            if po.state == 'draft' and len(po.statement_ids) != 0:
                raise osv.except_osv(
                    _('Error!'),
                    _("You can not invoice a partial paid POS Order"))
            if po.amount_total == 0:
                raise osv.except_osv(
                    _('Error!'),
                    _("You can not invoice an empty POS Order"))
        res = super(PosOrder, self).action_invoice(
            cr, uid, ids, context=context)
        for po in self.browse(cr, uid, ids, context=context):
            forbid_payment = po.state == 'invoiced' and\
                len(po.statement_ids) != 0
            inv_obj.write(cr, uid, [po.invoice_id.id], {
                'forbid_payment': forbid_payment,
                'date_invoice': po.date_order,
            }, context=context)
            wf_service.trg_validate(
                uid, 'account.invoice', po.invoice_id.id,
                'invoice_open', cr)

        return res
