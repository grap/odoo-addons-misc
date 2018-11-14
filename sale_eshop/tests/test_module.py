# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.ResPartner = self.env['res.partner']
        self.ProductProduct = self.env['product.product']

    # Test Section
    def __test_01_login(self):
        res = self.ResPartner.login('admin@localhost', 'eshop_password')
        self.assertNotEqual(
            res, False, "Correct Credentials should be accepted")

        res = self.ResPartner.login('admin@localhost', 'bad_password')
        self.assertEqual(
            res, False, "Bad Credentials should be refused")

        res = self.ResPartner.login('admin@localhost', 'admin')
        self.assertNotEqual(
            res, False, "Addmin Password should be accepted")

    def test_02_load_products(self):
        result = self.ProductProduct.get_current_eshop_product_list()
        self.assertNotEqual(
            len(result), 0, "Loading products should return a non empty list")
