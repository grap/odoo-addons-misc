# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class AccountVoucher(Model):
    _inherit = 'account.voucher'

    # Override section
    def recompute_voucher_lines(
            self, cr, uid, ids, partner_id, journal_id, price, currency_id,
            ttype, date, context=None):
        res = super(AccountVoucher, self).recompute_voucher_lines(
            cr, uid, ids, partner_id, journal_id, price, currency_id, ttype,
            date, context=context)
        aml_obj = self.pool.get('account.move.line')
        inv_obj = self.pool.get('account.invoice')
        for item in ['line_dr_ids', 'line_cr_ids']:
            for line in res['value'][item]:
                aml_id = line['move_line_id']
                if not aml_id:
                    continue
                aml = aml_obj.browse(cr, uid, aml_id, context=context)
                am_id = aml.move_id.id
                inv_ids = inv_obj.search(
                    cr, uid, [('move_id', '=', am_id)], context=context)
                inv_id = inv_ids and inv_ids[0] or False
                if not inv_id:
                    continue
                inv = inv_obj.browse(cr, uid, inv_id, context=context)
                if inv.forbid_payment:
                    res['value'][item].remove(line)
        return res
