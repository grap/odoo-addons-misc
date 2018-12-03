# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.eshop_user = self.env.ref('sale_eshop.eshop_user')
        self.ResPartner = self.env['res.partner'].sudo(self.eshop_user)
        self.SaleOrder = self.env['sale.order'].sudo(self.eshop_user)
        self.ProductProduct = self.env['product.product'].sudo(self.eshop_user)
        self.customer = self.env.ref('base.partner_root')
        self.banana = self.env.ref('sale_eshop.product_banana')
        self.apple = self.env.ref('sale_eshop.product_apple')
        self.product_disabled = self.env.ref('sale_eshop.product_disabled')
        self.product_not_available = self.env.ref('stock.product_icecream')

    # Test Section
    def test_01_login(self):
        res = self.ResPartner.login(self.customer.email, 'eshop_password')
        self.assertNotEqual(
            res, False, "Correct Credentials should be accepted")

        res = self.ResPartner.login(self.customer.email, 'bad_password')
        self.assertEqual(
            res, False, "Bad Credentials should be refused")

        res = self.ResPartner.login(self.customer.email, 'admin')
        self.assertNotEqual(
            res, False, "Addmin Password should be accepted")

    def test_02_load_products(self):
        result = self.ProductProduct.get_current_eshop_product_list()
        self.assertNotEqual(
            len(result), 0, "Loading products should return a non empty list")

    def test_03_product_available(self):
        self.assertEqual(
            self.product_not_available.eshop_state, 'unavailable',
            "Bad state for unavailable product")

        self.assertEqual(
            self.banana.eshop_state, 'available',
            "Bad state for available product")

        self.assertEqual(
            self.product_disabled.eshop_state, 'disabled',
            "Bad state for disabled product")

    def test_03_sale_order_process(self):
        # Create Order
        self.SaleOrder.eshop_set_quantity(
            self.customer.id, self.banana.id, 3, 'add')
        order_id = self.SaleOrder.eshop_get_current_sale_order_id(
            self.customer.id)
        self.assertNotEqual(
            order_id, False,
            "Adding a product for a customer that don't have sale order"
            " should create a new sale order")

        # Add quantity to the same product
        self.SaleOrder.eshop_set_quantity(
            self.customer.id, self.banana.id, 2, 'add')
        order = self.SaleOrder.browse(order_id)
        order_line = order.order_line[0]
        self.assertEqual(
            order_line.product_uom_qty, 5,
            "Adding a quantity should sum with the previous quantity")

        # set new quantity to the same product
        self.SaleOrder.eshop_set_quantity(
            self.customer.id, self.banana.id, 1, 'set')
        self.assertEqual(
            order_line.product_uom_qty, 1,
            "setting a quantity should erase previous quantity")

        # Finish the order
        order.eshop_set_as_sent()
        self.assertEqual(
            order.state, 'sent',
            "Finishing an order in the eshop should set the order as 'sent'")

        # Simulate cron
        self.SaleOrder.sudo()._eshop_cron_confirm_orders()
        self.assertNotEqual(
            order.state, 'sent',
            "Once cron has been run, orders should not be in 'sent' state.")
