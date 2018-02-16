# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

_INTERNAL_USE_STATE = [
    ('draft', 'New'),
    ('confirmed', 'Confirmed'),
    ('done', 'Done'),
]


class InternalUse(models.Model):
    _name = 'internal.use'
    _order = 'date_done desc, name'

    # Columns section
    name = fields.Char(string='Name', required=True, default='/')

    description = fields.Char(
        string='Description', states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]})

    date_done = fields.Date(
        string='Date', required=True,
        default=lambda *x: time.strftime('%Y-%m-%d'),
        states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]})

    internal_use_case_id = fields.Many2one(
        comodel_name='internal.use.case', string='Case', required=True,
        states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]},
        oldname='internal_use_case')

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True,
        related='internal_use_case_id.company_id', store=True)

    state = fields.Selection(
        selection=_INTERNAL_USE_STATE, string='Status', readonly=True,
        state='draft')

    line_ids = fields.One2many(
        comodel_name='internal.use.line', inverse_name='internal_use_id',
        copy=False,
        string='Lines', states={
            'done': [('readonly', True)],
            'confirmed': [('readonly', True)]})

    # TODO migration for old picking_id (and related stock.moves)
    stock_move_ids = fields.One2many(
        comodel_name='stock.move', inverse_name='internal_use_id',
        string='Stock moves', copy=False)

    account_move_id = fields.Many2one(
        comodel_name='account.move', string='Account Moves', readonly=True,
        copy=False)

    amount = fields.Float(
        string='Total Amount (Tax excluded)', compute='_compute_amount',
        store=True)

    # Compute Section
    @api.depends('state', 'line_ids', 'line_ids.amount')
    def _compute_amount(self):
        for use in self:
            use.amount = sum(use.mapped('line_ids.amount'))

    # Overload Section
    @api.model
    def create(self, vals):
        sequence_obj = self.env['ir.sequence']
        vals['name'] = sequence_obj.get('internal.use')
        return super(InternalUse, self).create(vals)

    @api.multi
    def unlink(self):
        if self.filtered(lambda x: x.state != 'draft'):
            raise UserError(_('You can only delete draft uses.'))
        return super(InternalUse, self).unlink()

    # Actions section
    @api.multi
    def action_confirm(self):
        """ Set the internal use to 'confirmed' and create stock moves"""
        stock_move_obj = self.env['stock.move']
        for use in self:
            if len(use.line_ids) == 0:
                raise UserError(_(
                    "You can not confirm an empty Internal Use."))

            # Create stock moves
            for line in use.line_ids:
                stock_move_obj.create(line._prepare_stock_move())

            # Confirm stock moves
            use.stock_move_ids.action_done()

        # Mark the use as 'confirmed'
        return self.write({'state': 'confirmed'})

    @api.multi
    def action_done(self):
        """ Set the internal use to 'done' and create account moves"""
        account_move_obj = self.env['account.move']
        use_line_obj = self.env['internal.use.line']

        use_data = {}

        for use in self:
            key = use._get_expense_entry_key()

            if key in use_data.keys():
                use_data[key].append(use.id)
            else:
                use_data[key] = [use.id]

        for key, use_ids in use_data.iteritems():
            uses = self.browse(use_ids)
            # prepare Account Move
            account_move_vals = uses._prepare_account_move()

            # Create Main Account Move Line
            account_move_line_vals = uses._prepare_account_move_line(
                account_move_vals)
            all_account_move_line_vals = [(0, 0, account_move_line_vals)]

            # Create Counterpart Account Move Line(s)
            use_line_data = {}
            for line in uses.mapped('line_ids'):
                line_key = line._get_expense_entry_key()

                if line_key in use_line_data:
                    use_line_data[line_key].append(line.id)
                else:
                    use_line_data[line_key] = [line.id]

            for line_key, line_ids in use_line_data.iteritems():
                lines = use_line_obj.browse(line_ids)
                account_move_line_vals = lines._prepare_account_move_line(
                    account_move_vals)
                all_account_move_line_vals.append(
                    (0, 0, account_move_line_vals))

            # Create Account move and validate it
            account_move_vals['line_id'] = all_account_move_line_vals
            print account_move_vals
            account_move = account_move_obj.create(account_move_vals)

            # Validate Account Move
            account_move.button_validate()

            # associate internal uses to account move and set to 'done'
            uses.write({
                'state': 'done',
                'account_move_id': account_move.id,
            })

        return True

    # Custom Section
    @api.multi
    def _get_expense_entry_key(self):
        """
            define how to group by uses to generate a unique Journal Entry.
            By default, an entry is generated by use case and by month.
            Overwrite this function to change the behaviour.
            Note that internal_use_case_id is mandatory.
        """
        self.ensure_one()
        dt = fields.Date.from_string(self.date_done)
        return (
            self.internal_use_case_id.id,
            '%d-%d' % (dt.year, dt.month),
        )

    @api.multi
    def _prepare_account_move(self):
        use_case = self[0].internal_use_case_id
        period_obj = self.env['account.period']
        period = period_obj.find(dt=self[0].date_done)
        return {
            'journal_id': use_case.journal_id.id,
            'company_id': use_case.company_id.id,
            'date': period.date_stop,
            'period_id': period.id,
            'ref': _('Expense Transfert (%s)') % (use_case.name),
        }

    @api.multi
    def _prepare_account_move_line(self, account_move_vals):
        use_case = self[0].internal_use_case_id
        total = sum(self.mapped('amount'))
        return {
            'name': _('Expense Transfert (%s)') % (use_case.name),
            'date': account_move_vals['date'],
            'period_id': account_move_vals['period_id'],
            'account_id': use_case.account_id.id,
            'debit': (total > 0) and total or 0,
            'credit': (total < 0) and -total or 0,
        }
