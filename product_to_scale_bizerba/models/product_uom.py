# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductUom(models.Model):
    _inherit = 'product.uom'

    scale_type = fields.Char(
        string='Scale Type', help="Letter that indicates how the product"
        " send to Bizerba will be handled:\n"
        " 'P': Weightable Product. the label edited by scales will mention"
        " the price, depending on the weight of the product\n"
        " 'Q': Quantity. The label edited by scales will mention the"
        " price, depending on the quantity entered by the operator")
