# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):
    """Tests for 'Stock Picking - Quick Edit' Module"""

    def setUp(self):
        super(TestModule, self).setUp()
        self.wizard_obj = self.env['stock.picking.quick.edit.wizard']
        self.new_move_obj = self.env[
            'stock.picking.quick.edit.wizard.new.move']
        self.picking = self.env.ref('stock.incomming_chicago_warehouse3')
        self.wizard = self.wizard_obj.with_context(
            active_id=self.picking.id).create({})
        self.product = self.env.ref('product.product_product_7')

    # Test Section
    def test_01_wizard_change_move(self):
        existing_move = self.wizard.current_move_ids[0]
        existing_move.product_uom_qty = 999
        self.wizard.apply()
        self.assertEqual(
            self.picking.move_lines[0].product_uom_qty,
            999,
            "Wizard failed to change the move quantity")

    def test_02_wizard_add_move(self):
        self.new_move_obj.create({
            'wizard_id': self.wizard.id,
            'product_id': self.product.id,
            'product_uom_qty': 777,
            'product_uom_id': self.product.uom_id.id,
        })
        self.wizard.apply()
        self.assertEqual(
            len(self.picking.move_lines), 2,
            "Adding new line in wizard should add a new line in picking")
        new_moves = self.picking.move_lines.filtered(
            lambda x: x.product_id.id == self.product.id and
            x.product_uom_qty == 777)
        self.assertEqual(
            len(new_moves), 1,
            "The new line has not been added correctly")
