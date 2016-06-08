# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class PosSwitchJournalWizard(models.TransientModel):
    _name = 'pos.switch.journal.wizard'

    @api.model
    def _selection_new_statement_id(self):
        statement_line_obj = self.env['account.bank.statement.line']

        if self.env.context.get('active_model', False)\
                != 'account.bank.statement.line':
            return True

        statement_line = statement_line_obj.browse(
            self.env.context.get('active_id'))
        statements = statement_line.mapped(
            'pos_statement_id.session_id.statement_ids')
        return [
            (s.id, s.journal_id.name)
            for s in statements if s.id != statement_line.statement_id.id]

    # Column Section
    statement_line_id = fields.Many2one(
        comodel_name='account.bank.statement.line', string='Statement',
        required=True, readonly=True)
    old_journal_id = fields.Many2one(
        comodel_name='account.journal', string='Old Journal', required=True,
        readonly=True)
    amount = fields.Float(
        string='Amount', readonly=True)
    new_statement_id = fields.Selection(
        selection=_selection_new_statement_id, string='New Journal',
        required=True)

    @api.model
    def default_get(self, fields):
        statement_line_obj = self.env['account.bank.statement.line']
        res = super(PosSwitchJournalWizard, self).default_get(fields)
        statement_line = statement_line_obj.browse(
            self.env.context.get('active_id'))
        res.update({
            'statement_line_id': statement_line.id,
            'old_journal_id': statement_line.journal_id.id,
            'amount': statement_line.amount,
        })
        return res

    # Action section
    @api.multi
    def button_switch_journal(self):
        statement_line_obj = self.env['account.bank.statement.line']

        wizard = self[0]
        statement_line = statement_line_obj.browse(wizard.statement_line_id.id)
        statement_line.pos_statement_id._allow_change_payments()
        amount = statement_line.amount

        ctx = self.env.context.copy()
        ctx['change_pos_payment'] = True

        statement_line.with_context(ctx).write({
            'amount': amount,
            'statement_id': int(wizard.new_statement_id),
        })
