# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp.osv.orm import Model

_logger = logging.getLogger(__name__)


class PosSession(Model):
    _inherit = 'pos.session'

    def wkf_action_close(self, cr, uid, ids, context=None):
        po_obj = self.pool['pos.order']
        aml_obj = self.pool['account.move.line']

        # Call regular workflow
        res = super(PosSession, self).wkf_action_close(
            cr, uid, ids, context=context)

        # Get All Pos Order invoiced during the current Sessions
        po_ids = po_obj.search(cr, uid, [
            ('session_id', 'in', ids),
            ('invoice_id', '!=', False),
        ], context=context)
        for po in po_obj.browse(cr, uid, po_ids, context=context):
            # We're searching only account Invoices that has been payed
            # In Point Of Sale
            if not po.invoice_id.pos_pending_payment:
                continue

            # Search all move Line to reconcile in Sale Journal
            aml_sale_ids = []
            aml_sale_total = 0

            # Get accounting partner
            if po.partner_id.parent_id:
                partner = po.partner_id.parent_id
            else:
                partner = po.partner_id

            for aml in po.invoice_id.move_id.line_id:
                if (aml.partner_id.id == partner.id and
                        aml.account_id.type == 'receivable'):
                    aml_sale_ids.append(aml.id)
                    aml_sale_total += aml.debit - aml.credit

            aml_payment_ids = []
            aml_payment_total = 0
            # Search all move Line to reconcile in Payment Journals
            abs_ids = list(set([x.statement_id.id for x in po.statement_ids]))
            aml_ids = aml_obj.search(cr, uid, [
                ('statement_id', 'in', abs_ids),
                ('partner_id', '=', partner.id),
                ('reconcile_id', '=', False)], context=context)
            for aml in aml_obj.browse(
                    cr, uid, aml_ids, context=context):
                if (aml.account_id.type == 'receivable'):
                    aml_payment_ids.append(aml.id)
                    aml_payment_total += aml.debit - aml.credit

            # Try to reconcile
            if aml_payment_total != - aml_sale_total:
                # Unable to reconcile
                print "----- PAS BIEN"
                _logger.warning(
                    "Unable to reconcile the payment of %s #%s."
                    "(partner : %s)" % (
                        po.name, po.id, partner.name))
            else:
                print "!!!! BIEN !!!"
                aml_obj.reconcile(
                    cr, uid, aml_payment_ids + aml_sale_ids, 'manual',
                    False, False, False, context=context)

        return res
