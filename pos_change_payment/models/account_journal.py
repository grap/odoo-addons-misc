# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # Private Function Section
    @api.model
    def _get_pos_journal_selection(self, session_id):
        """Return Account Journal available for payment in PoS Module"""
        journal_obj = self.env['account.journal']
        session_obj = self.env['pos.session']

        # Get Session of the Current PoS
        session = session_obj.browse(session_id)

        # Get Journals, order by type (cash before), and name
        cash_journals = journal_obj.search(
            [('id', 'in', session.journal_ids.ids), ('type', '=', 'cash')],
            order='name')
        res = [(j.id, j.name) for j in cash_journals]

        other_journals = journal_obj.search(
            [('id', 'in', session.journal_ids.ids), ('type', '!=', 'cash')],
            order='name')
        res += [(j.id, j.name) for j in other_journals]


        return res
