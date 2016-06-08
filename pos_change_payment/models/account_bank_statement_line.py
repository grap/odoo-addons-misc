# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv.orm import Model
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class account_bank_statement_line(Model):
    _inherit = 'account.bank.statement.line'

    _POS_PAYMENT_ALLOW_WRITE = [
        'sequence', 'move_ids',
    ]

    # Private Function Section
    def _check_allow_change_pos_payment(
            self, cr, uid, ids, vals, context=None):
        """Allow or block change of account bank statement line, linked to
        a non draft POS Order.
            * if 'change_pos_payment' is in the context, changes are allowed;
            * otherwise:
                * allow write of some fields only;
            * forbid deletion;"""
        context = context or {}
        values = vals.copy() if vals else {}
        check_pos_order = False
        po_obj = self.pool['pos.order']

        if not ids:
            return True

        if values:
            # Allow some write
            for key in self._POS_PAYMENT_ALLOW_WRITE:
                if key in values:
                    del values[key]
            if not values:
                return True

        # Allow changes, if user use the wizard
        if context.get('change_pos_payment', False):
            check_pos_order = True

        for absl in self.browse(cr, uid, ids, context=context):
            if absl.pos_statement_id:
                if absl.pos_statement_id.state != 'draft':
                    if check_pos_order:
                        po_obj._allow_change_payments(
                            cr, uid, [absl.pos_statement_id.id],
                            context=context)
                    else:
                        if values.keys() == ['partner_id']:
                            po_obj._allow_change_payments(
                                cr, uid, [absl.pos_statement_id.id],
                                context=context)
                        else:
                            raise except_osv(
                                _('Error!'),
                                _("""You can not change payments of POS by"""
                                    """ this way. Please use the regular"""
                                    """ wizard in POS view!"""))
        return True

    # Overload Section
    def write(self, cr, uid, ids, vals, context=None):
        self._check_allow_change_pos_payment(
            cr, uid, ids, vals, context=context)
        res = super(account_bank_statement_line, self).write(
            cr, uid, ids, vals, context=context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        self._check_allow_change_pos_payment(
            cr, uid, ids, None, context=context)
        res = super(account_bank_statement_line, self).unlink(
            cr, uid, ids, context=context)
        return res
