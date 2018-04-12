# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductScaleLogWizard(models.TransientModel):
    _name = 'product.scale.log.wizard'

    _LOG_TYPE_SELECTION = [
        ('create', 'Create'),
        ('write', 'Update'),
        ('unlink', 'Unlink'),
    ]

    # Column Section
    product_qty = fields.Integer(
        string='Product Quantity', readonly=True,
        default=lambda s: s._default_product_qty())

    log_type = fields.Selection(
        _LOG_TYPE_SELECTION, string='Log Type', required=True,
        default='create')

    # Default Section
    @api.model
    def _default_product_qty(self):
        return len(self.env.context.get('active_ids', []))

    # View Section
    @api.multi
    def send_log(self):
        self.ensure_one()
        product_obj = self.env['product.product']
        products = product_obj.search([
            ('id', 'in', self.env.context.get('active_ids', [])),
            ('scale_group_id', '!=', False),
        ])
        if self.log_type == 'create':
            products.send_scale_create()
        elif self.log_type == 'write':
            products.send_scale_write()
        elif self.log_type == 'unlink':
            products.send_scale_unlink()
