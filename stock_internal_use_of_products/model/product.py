# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Internal Use Of Products for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv.orm import Model


class product_product(Model):
    _inherit = "product.product"

    def get_product_income_expense_accounts(
            self, cr, uid, product_id, context=None):
        """ To get the income and expense accounts related to product.
        @param product_id: product id
        @return: dictionary which contains information regarding
            income and expense accounts
        """
        if context is None:
            context = {}
        categ = self.pool.get('product.product').browse(
            cr, uid, product_id, context=context).categ_id
        product = self.browse(cr, uid, product_id, context=context)

        income_acc = product.property_account_income\
            and product.property_account_income.id or False
        if not income_acc:
            income_acc = categ.property_account_income_categ\
                and categ.property_account_income_categ.id or False

        expense_acc = product.property_account_expense\
            and product.property_account_expense.id or False
        if not expense_acc:
            expense_acc = categ.property_account_expense_categ\
                and categ.property_account_expense_categ.id or False

        return {
            'account_income': income_acc,
            'account_expense': expense_acc,
        }
