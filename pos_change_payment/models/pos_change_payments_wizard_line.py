# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class PosChangePaymentsWizardLine(models.TransientModel):
    _name = 'pos.change.payments.wizard.line'

    # Selection Section
    @api.model
    def _select_journals(self):
        import pdb; pdb.set_trace()
        res = []
        print ">>>>>>>>>>>>>>>>>>>>><<<"
        print self.env.context
        print ">>>>>>>>>>>>>>>>>>>>><"
#        journal_obj = self.env['account.journal']
#        wizard_obj = self.env['pos.change.payments.wizard']

#        wizard = wizard_obj.browse(self.env.context('field_parent'))
#        res = journal_obj._get_pos_journal_selection(
#            wizard.order_id.session_id.id)
#        print res
        return res

    # Column Section
    wizard_id = fields.Many2one(
        comodel_name='pos.change.payments.wizard', string='Wizard',
        ondelete='cascade')
    journal_id = fields.Selection(
        selection=_select_journals, string='Journal', required=True)
    amount = fields.Float(
        string='Amount', required=True)
