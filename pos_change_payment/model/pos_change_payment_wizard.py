# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Change Payment module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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

from openerp.osv import fields
from openerp.osv.osv import except_osv
from openerp.osv.orm import TransientModel
from openerp.tools.translate import _


class pos_change_payment_wizard(TransientModel):
    _name = 'pos.change.payment.wizard'

    def _get_new_statement_id(self, cr, uid, context=None):
        absl_obj = self.pool['account.bank.statement.line']
        abs_obj = self.pool['account.bank.statement']

        if context.get('active_model', False) != 'account.bank.statement.line':
            return True
        absl = absl_obj.browse(
            cr, uid, context.get('active_id'), context=context)
        abs_ids = [
            x.id for x in absl.pos_statement_id.session_id.statement_ids]

        res = abs_obj.read(
            cr, uid, abs_ids, ['id', 'journal_id'], context=context)
        res = [(
            r['id'], r['journal_id'][1])
            for r in res if r['id'] != absl.statement_id.id]
        return res

    _columns = {
        'statement_line_id': fields.many2one(
            'account.bank.statement.line', 'Statement',
            required=True, readonly=True),
        'old_journal_id': fields.many2one(
            'account.journal', 'Old Journal', required=True, readonly=True),
        'amount': fields.float('Amount', readonly=True),
        'new_statement_id': fields.selection(
            _get_new_statement_id, 'New Journal', required=True),
    }

    def default_get(self, cr, uid, fields, context=None):
        absl_obj = self.pool['account.bank.statement.line']
        if context.get('active_model', False) != 'account.bank.statement.line':
            raise except_osv(_('Error!'), _('Incorrect Call!'))
        res = super(pos_change_payment_wizard, self).default_get(
            cr, uid, fields, context=context)
        absl = absl_obj.browse(
            cr, uid, context.get('active_id'), context=context)
        res.update({'statement_line_id': absl.id})
        res.update({'old_journal_id': absl.journal_id.id})
        res.update({'amount': absl.amount})
        return res

    # Action section
    def button_change_payment(self, cr, uid, ids, context=None):
        absl_obj = self.pool['account.bank.statement.line']
        pcpw = self.browse(cr, uid, ids[0], context=context)
        absl = absl_obj.browse(
            cr, uid, pcpw.statement_line_id.id, context=context)
        if absl.pos_statement_id.state not in ('draft', 'paid'):
            raise except_osv(
                _('Error!'),
                _('You can only change statements of Draft or Paid Orders!'))
        amount = absl.amount
        # We do 2 write, one in the old statement, one in the new, with
        # 'amount' value each time to recompute all the functional fields
        # of the account.bank.statement object
        absl_obj.write(cr, uid, [absl.id], {
            'amount': 0,
        }, context=context)
        # Change statement of the statement line
        absl_obj.write(cr, uid, [absl.id], {
            'amount': amount,
            'statement_id': int(pcpw.new_statement_id),
        }, context=context)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
