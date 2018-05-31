# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductPrepareCategory(models.Model):
    _name = 'product.prepare.category'
    _order = 'sequence, name'

    # Default Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    # Column Section
    name = fields.Char(string='Name', required=True)

    sequence = fields.Integer(string='Sequence', required=True)

    code = fields.Char(string='Code', required=True, size=5)

    color = fields.Char(string='Color', required=True, default='#FFFFFF')

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=_default_company_id)

    active = fields.Boolean(string='Active', default=True)

    product_ids = fields.One2many(
        comodel_name='product.product', inverse_name='prepare_categ_id',
        string='Products')
