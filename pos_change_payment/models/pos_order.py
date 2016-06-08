# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, exceptions


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def _merge_cash_payment(self):
        statement_line_obj = self.env['account.bank.statement.line']
        for order in self:
            absl_cash_ids = [
                x.id for x in order.statement_ids
                if x.statement_id.journal_id.type == 'cash']
            new_payments = {}
            for line in statement_line_obj.read(
                    absl_cash_ids, ['statement_id', 'amount']):
                if line['statement_id'][0] in new_payments.keys():
                    new_payments[line['statement_id'][0]] += line['amount']
                else:
                    new_payments[line['statement_id'][0]] = line['amount']

            # Delete all obsolete account bank statement line
            statement_line_obj.unlink(absl_cash_ids)

            # Create a new one
            for k, v in new_payments.items():
                self.add_payment(order.id, {
                    'statement_id': k,
                    'amount': v
                })

    # Overload Section
    @api.multi
    def action_paid(self):
        """ Merge all cash statement line of the Order"""
        ctx = self.env.context.copy()
        ctx['change_pos_payment'] = True
        self.with_context(ctx)._merge_cash_payment()
        return super(PosOrder, self).action_paid()

    # Private Function Section
    @api.multi
    def _allow_change_payments(self):
        """Raise an error if the user can not change the payment of a POS
        because of current session state."""
        for order in self:
            if order.session_id.state == 'closed':
                raise ValidationError(
                    _("You can not change payments of the POS '%s' because"
                        " the associated session '%s' has been closed!") % (
                            order.name, order.session_id.name))
