# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):
    """Tests for 'Stock Picking - Mass Change' Module"""

    def setUp(self):
        super(TestModule, self).setUp()
        self.wizard_obj = self.env['stock.picking.mass.change.wizard']
        self.picking_1 = self.env.ref('stock_picking_mass_change.picking_1')
        self.picking_2 = self.env.ref('stock_picking_mass_change.picking_2')
        self.product = self.env.ref('product.product_product_9')

    # Test Section
    def test_01_wizard_pro_rata(self):
        wizard = self._create_wizard('pro_rata', 150, 1)
        wizard.button_apply()
        self.assertEqual(
            self.picking_1.move_lines[0].product_uom_qty,
            100,
            "Incorrect computation of the new qty for prorata method. (1/2)")
        self.assertEqual(
            self.picking_2.move_lines[0].product_uom_qty,
            50,
            "Incorrect computation of the new qty for prorata method. (2/2)")

    def test_01_wizard_fifo(self):
        wizard = self._create_wizard('fifo', 230, 1)
        wizard.button_apply()
        self.assertEqual(
            self.picking_1.move_lines[0].product_uom_qty,
            200,
            "Incorrect computation of the new qty for fifo method. (1/2)")
        self.assertEqual(
            self.picking_2.move_lines[0].product_uom_qty,
            30,
            "Incorrect computation of the new qty for fifo method. (2/2)")

    def _create_wizard(self, change_method, target_product_qty, rounding):
        wizard = self.wizard_obj.with_context(
            active_ids=[self.picking_1.id, self.picking_2.id]).create({
                'product_id': self.product.id,
            })
        wizard.onchange_product_id()
        wizard.write({
            'change_method': change_method,
            'rounding': rounding,
            'target_product_qty': target_product_qty,
        })
        wizard.onchange_change_setting()
        return wizard
