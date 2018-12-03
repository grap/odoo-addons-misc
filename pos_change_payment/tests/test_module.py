# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
# from openerp.exceptions import Warning as UserError


class TestModule(TransactionCase):
    """Tests for 'Point of Sale - Change Payment' Module"""

    def setUp(self):
        super(TestModule, self).setUp()
        self.PosSession = self.env['pos.session']
        self.PosOrder = self.env['pos.order']
        self.PosMakePayment = self.env['pos.make.payment']
        self.PosSwitchJournalWizard = self.env['pos.switch.journal.wizard']
        self.product = self.env.ref('product.product_product_3')
        self.pos_config = self.env.ref('point_of_sale.pos_config_main')
        self.check_journal = self.env.ref('account.check_journal')
        self.cash_journal = self.env.ref('account.cash_journal')

        # create new session and open it
        self.session = self.PosSession.create(
            {'config_id': self.pos_config.id})
        self.session.open_cb()
        self.check_statement = self.session.statement_ids.filtered(
            lambda x: x.journal_id == self.check_journal)
        self.cash_statement = self.session.statement_ids.filtered(
            lambda x: x.journal_id == self.cash_journal)

    def _sale(self, session, journal_1, price_1, journal_2=False, price_2=0.0):
        order = self.PosOrder.create({
            'session_id': session.id,
            'lines': [[0, False, {
                'name': 'OL/0001',
                'product_id': self.product.id,
                'qty': 1.0,
                'price_unit': price_1 + price_2,
            }]],
        })
        payment = self.PosMakePayment.create({
            'journal_id': journal_1.id,
            'amount': price_1,
        })
        if journal_2:
            self.PosMakePayment.create({
                'journal_id': journal_2.id,
                'amount': price_2,
            })
        payment.with_context(active_id=order.id).check()
        return order

    # Test Section
    def test_01_pos_switch_journal(self):
        # Make a sale with 100 in cash journal
        order = self._sale(self.session, self.cash_journal, 100)
        statement_line = order.statement_ids[0]

        # Switch to check journal
        wizard = self.PosSwitchJournalWizard.with_context(
            active_id=statement_line.id).create({
                'new_journal_id': self.check_journal.id,
            })
        wizard.button_switch_journal()

        self.assertEqual(
            len(order.statement_ids.filtered(
                lambda x: x.journal_id == self.cash_journal)), 0,
            "Altered order should not have the original payment journal")

        self.assertEqual(
            len(order.statement_ids.filtered(
                lambda x: x.journal_id == self.check_journal)), 1,
            "Altered order should have the final payment journal")
