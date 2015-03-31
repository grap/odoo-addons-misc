# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Merge Moves By Patterns for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

import logging
from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.osv import osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class account_merge_pattern(Model):
    _description = 'Account Merge Pattern'
    _name = 'account.merge.pattern'

    # Columns section
    _columns = {
        'name': fields.char('Name', size=128, required=True,),
        'active': fields.boolean(
            'Active', help="""By unchecking this field, you can easily"""
            """ disable a pattern without deleting it."""),
        'company_id': fields.many2one(
            'res.company', 'Company', required=True, readonly=True,
            help="Select the company of the pattern."),
        'journal_id': fields.many2one(
            'account.journal', 'Journal', required=True,
            help="""Select a journal.\nThe request for merging the account"""
            """ move will be realized only for this journal """),
        'output_journal_id': fields.many2one(
            'account.journal', 'Output Journal', required=True,
            help="""Select a journal.\nThe acount move of merge will be"""
            """ wroten in this journal """),
        'debit_account_ids': fields.many2many(
            'account.account', 'account_merge_pattern_debit_account_rel',
            'pattern_id', 'account_id', 'Debit Accounts',
            help="""Select the debit accounts of the pattern.\nAn account"""
            """ move will be selected if it perfectly matches the defined"""
            """ pattern."""),
        'credit_account_ids': fields.many2many(
            'account.account', 'account_merge_pattern_credit_account_rel',
            'pattern_id', 'account_id', 'Debit Accounts',
            help="""Select the credit accounts of the pattern.\nAn account"""
            """ move will be selected if it perfectly matches the defined"""
            """ pattern."""),
        'period_ids': fields.many2many(
            'account.period', 'account_merge_pattern_account_rel',
            'pattern_id', 'period_id', 'Period to Merge',
            help="""Select the period that will be affected by the 'merge'"""
            """ button.\nBy default, select all the opened periods."""),
        'ref_pattern': fields.char(
            'Reference Pattern', size=128, required=True,
            help="""Tip a text that will be used in each account move for"""
            """ the 'ref' field."""),
        'name_line_pattern': fields.char(
            'Name Line Pattern', size=128, required=True,
            help="""Tip a text that will be used in each account move line"""
            """ for the 'name' field."""),
    }

    # Default section
    _defaults = {
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
        'active': True,
    }

    # Constraints Section
    def _check_journal_company_id(self, cr, uid, ids, context=None):
        for amp in self.browse(cr, uid, ids, context=context):
            if (amp.company_id.id != amp.journal_id.company_id.id):
                return False
        return True

    def _check_account_company_id(self, cr, uid, ids, context=None):
        for amp in self.browse(cr, uid, ids, context=context):
            for account in amp.debit_account_ids:
                if (amp.company_id.id != account.company_id.id):
                    return False
            for account in amp.credit_account_ids:
                if (amp.company_id.id != account.company_id.id):
                    return False
        return True

    def _check_period_company_id(self, cr, uid, ids, context=None):
        for amp in self.browse(cr, uid, ids, context=context):
            for period in amp.period_ids:
                if (amp.company_id.id != period.company_id.id):
                    return False
        return True

    _constraints = [
        (
            _check_journal_company_id,
            """Error: Account Journal and Account Merge Pattern must belong"""
            """ to the same company.""",
            ['journal_id', 'company_id', ]),
        (
            _check_account_company_id,
            """Error: Debits / Credits Accounts and Account Merge Pattern"""
            """ must belong to the same company.""",
            ['debit_account_ids', 'credit_account_ids', 'company_id', ]),
        (
            _check_period_company_id, """Error: Account Periods and Account"""
            """ Merge Pattern must belong to the same company.""",
            ['period_ids', 'company_id', ]),
    ]

    # Cron Section
    def cron_merge_account_moves(self, cr, uid, ids, context=None):
        """
            Public function call by cron task to merge account moves.
            This function change user company in each call to avoid bad
            context.
        """
        for amp in self.browse(cr, uid, ids, context=context):
            # Changing company_id of the user
            self.pool.get('res.users').write(
                cr, uid, [uid], {'company_id': amp.company_id.id},
                context=context)
            self._merge_account_moves(cr, uid, [amp.id], context=context)

    # Actions Section
    def action_merge_account_moves(self, cr, uid, ids, context=None):
        self._merge_account_moves(cr, uid, ids, context=context)
        return True

    # Private Function Section
    def _get_account_move_line(
            self, cr, uid, account_move, account_id, context=None):
        for aml in account_move.line_id:
            if aml.account_id.id == account_id:
                return aml
        return None

    def _merge_account_moves(self, cr, uid, ids, context=None):
        am_obj = self.pool['account.move']
        ap_obj = self.pool['account.period']
        rc_obj = self.pool['res.company']
        for amp in self.browse(cr, uid, ids, context=context):
            rc_ids = rc_obj.search(cr, uid, [
                '|',
                ('parent_id', '=', amp.company_id.id),
                ('id', '=', amp.company_id.id)],
                context=context)
            # Merging by company_id
            for rc in rc_obj.browse(cr, uid, rc_ids, context=context):
                # merging by Opened Period
                all_ap_ids = [x.id for x in amp.period_ids]
                ap_ids = ap_obj.search(cr, uid, [
                    ('id', 'in', all_ap_ids),
                    ('state', '=', 'draft')],
                    context=context)
                for ap in ap_obj.browse(cr, uid, ap_ids, context=context):
                    _logger.info(
                        """Merging Moves. Pattern '%s'; Company '%s';"""
                        """ Period: '%s'""" % (amp.name, rc.name, ap.name))
                    narration = ''
                    account_move_ids_to_merge = []
                    account_move_lines = []
                    am_match_ids = []
                    debit_account_values = {}
                    credit_account_values = {}
                    max_date = ap.date_start

                    # Initialize the total of debit and credit values
                    for account_id in amp.debit_account_ids:
                        debit_account_values = {account_id.id: 0}
                    for account_id in amp.credit_account_ids:
                        credit_account_values = {account_id.id: 0}

                    # Filter to keep account moves matching the pattern
                    am_ids = am_obj.search(
                        cr, uid, [
                            ('journal_id', '=', amp.journal_id.id),
                            ('period_id', '=', ap.id),
                            ('company_id', '=', rc.id),
                            ('state', '=', 'posted'), ], context=context)
                    for am in am_obj.browse(cr, uid, am_ids, context=context):
                        match = True
                        for aml in am.line_id:
                            match = (match and(
                                (aml.credit and not aml.debit and
                                    aml.account_id in
                                    amp.credit_account_ids) or
                                (aml.debit and not aml.credit and
                                    aml.account_id in amp.debit_account_ids)))

                        if match and not am.merged_move_quantity:
                            account_move_ids_to_merge.append(am.id)

                            # compute the total of debit and credits values
                            for aml in am.line_id:
                                if aml.debit:
                                    debit_account_values[aml.account_id.id]\
                                        += aml.debit
                                elif aml.credit:
                                    credit_account_values[aml.account_id.id]\
                                        += aml.credit
                            narration += _(
                                """%s - Merged Account Move # %s"""
                                """ (date : %s) ; \n""") % (
                                fields.date.context_today(
                                    self, cr, uid, context=context),
                                am.name, am.date,)

                            # compute max date
                            max_date = max(max_date, am.date)

                    # Filter to get merging account move, if exists
                    am_ids = am_obj.search(
                        cr, uid, [
                            ('journal_id', '=', amp.output_journal_id.id),
                            ('period_id', '=', ap.id),
                            ('company_id', '=', rc.id),
                            ('merged_move_quantity', '!=', 0)],
                        context=context)
                    for am in am_obj.browse(cr, uid, am_ids, context=context):
                        match = True
                        for aml in am.line_id:
                            match = (match and (
                                (aml.credit and not aml.debit and
                                    aml.account_id in
                                    amp.credit_account_ids) or
                                (aml.debit and not aml.credit and
                                    aml.account_id in amp.debit_account_ids)))
                        if match:
                            am_match_ids.append(am.id)
                    if len(am_match_ids) == 0:
                        merge_account_move = None
                    elif len(am_match_ids) == 1:
                        merge_account_move = am_obj.browse(
                            cr, uid, am_ids[0], context=context)
                    else:
                        raise osv.except_osv(_('Error'), _(
                            """There is too merging account moves for"""
                            """ the company :'%s', period : '%s', journal"""
                            """ : '%s'""") % (
                            amp.company_id.name, ap.name,
                            amp.output_journal_id.name))

                    if account_move_ids_to_merge:
                        if not merge_account_move:
                            # creating new merge account move
                            for am_id in amp.debit_account_ids:
                                account_move_lines.append((0, 0, {
                                    'name': amp.name_line_pattern + _(
                                        '(%s Items)') % (
                                        len(account_move_ids_to_merge)),
                                    'date': max_date,
                                    'account_id': am_id.id,
                                    'debit': debit_account_values[am_id.id],
                                }))
                            for am_id in amp.credit_account_ids:
                                account_move_lines.append((0, 0, {
                                    'name': amp.name_line_pattern + _(
                                        '(%s Items)') % (
                                        len(account_move_ids_to_merge)),
                                    'date': max_date,
                                    'account_id': am_id.id,
                                    'credit': credit_account_values[am_id.id],
                                }))
                            account_move_id = am_obj.create(cr, uid, {
                                'company_id': rc.id,
                                'date': max_date,
                                'period_id': ap.id,
                                'journal_id': amp.output_journal_id.id,
                                'line_id': account_move_lines,
                                'ref': amp.ref_pattern,
                                'merged_narration': narration,
                                'merged_move_quantity':
                                len(account_move_ids_to_merge),
                            }, context=context)
                            am_obj.button_validate(
                                cr, uid, [account_move_id], context=context)
                        else:
                            # updating existing merge account move
                            am_obj.button_cancel(
                                cr, uid, [merge_account_move.id],
                                context=context)
                            line_id = []
                            for am_id in amp.credit_account_ids:
                                aml = self._get_account_move_line(
                                    cr, uid, merge_account_move, am_id.id,
                                    context=context)
                                line_id.append([1, aml.id, {
                                    'date': max(
                                        max_date, merge_account_move.date),
                                    'credit':
                                    aml.credit +
                                    credit_account_values[am_id.id],
                                    'name': amp.name_line_pattern + _(
                                        '(%s Items)') % (
                                        merge_account_move
                                        .merged_move_quantity +
                                        len(account_move_ids_to_merge)),
                                }])
                            for am_id in amp.debit_account_ids:
                                aml = self._get_account_move_line(
                                    cr, uid, merge_account_move, am_id.id,
                                    context=context)
                                line_id.append([1, aml.id, {
                                    'date': max(
                                        max_date, merge_account_move.date),
                                    'debit':
                                    aml.debit +
                                    debit_account_values[am_id.id],
                                    'name': amp.name_line_pattern + _(
                                        '(%s Items)') % (
                                        merge_account_move
                                        .merged_move_quantity +
                                        len(account_move_ids_to_merge)),
                                }])
                            vals = {
                                'line_id': line_id,
                                'date': max(max_date, merge_account_move.date),
                                'merged_narration':
                                merge_account_move.merged_narration +
                                '\n' + narration,
                                'merged_move_quantity':
                                merge_account_move.merged_move_quantity +
                                len(account_move_ids_to_merge),
                            }
                            am_obj.write(
                                cr, uid, [merge_account_move.id], vals,
                                context=context)
                            am_obj.button_validate(
                                cr, uid, [merge_account_move.id],
                                context=context)

                        # delete obsolete account move
                        _logger.info(
                            """Cancelling and deleting %s Moves."""
                            """ Pattern '%s'; Company '%s'; Period: '%s'""" % (
                                len(account_move_ids_to_merge), amp.name,
                                rc.name, ap.name))
                        am_obj.button_cancel(
                            cr, uid, account_move_ids_to_merge,
                            context=context)
                        am_obj.unlink(
                            cr, uid, account_move_ids_to_merge,
                            context=context)
