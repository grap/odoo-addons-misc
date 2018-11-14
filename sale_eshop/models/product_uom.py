# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductUom(models.Model):
    _name = 'product.uom'
    _inherit = ['product.uom', 'eshop.mixin']

    # Inherit Section
    _eshop_invalidation_type = 'multiple'

    _eshop_invalidation_fields = ['id', 'name', 'eshop_description']

    # Fields Section
    eshop_description = fields.Char('Description for the eShop')

    # Overload Section
    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        self._write_eshop_invalidate(vals)
        return super(ProductUom, self).write(vals)
