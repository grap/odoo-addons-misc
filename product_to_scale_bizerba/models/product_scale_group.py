# coding: utf-8
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductScaleGroup(models.Model):
    _name = 'product.scale.group'

    # Column Section
    name = fields.Char(string='Name', required=True)

    active = fields.Boolean(string='Active', default=True)

    external_shelf_id = fields.Char(
        string='External Shelf ID', required=True, default=1,
        help="Unused field for the time being. Define shelf products.")

    external_family_id = fields.Char(
        string='External Family ID', required=True, default=1,
        help="this value will be used in the KEY file, send to Scales, that"
        " specify production position on Customer Scale.")

    screen_display = fields.Boolean(
        string='Display on Screen', help="Check this box if you want"
        " to display the products on Customer Scale.")

    screen_obsolete = fields.Boolean(
        string='Screen Obsolete', readonly=True, default=False,
        help="This box is checked if the display of screen is obsolete")

    screen_offset = fields.Integer(string='Screen Offset')

    last_product_position = fields.Integer(
        compute='_compute_last_product_position',
        string='Last Product Position')

    screen_product_qty = fields.Integer(
        string='Products quantity on Screen', help="Set the number of"
        " products available for this Scale group.\n"
        " Set 0, if your scale do not have tactile screen.")

    company_id = fields.Many2one(
        related='scale_system_id.company_id', store=True,
        comodel_name='res.company', string='Company', readonly='True')

    scale_system_id = fields.Many2one(
        comodel_name='product.scale.system', string='Scale System',
        required=True)

    product_ids = fields.One2many(
        comodel_name='product.product', inverse_name='scale_group_id',
        string='Products')

    product_qty = fields.Integer(
        compute='_compute_product_qty', string='Products Quantity')

    # Compute Section
    @api.multi
    @api.depends('product_ids.scale_group_id')
    def _compute_product_qty(self):
        for group in self:
            group.product_qty = len(group.product_ids)

    @api.multi
    @api.depends('screen_offset', 'screen_product_qty')
    def _compute_last_product_position(self):
        for group in self:
            group.last_product_position =\
                group.screen_offset + group.screen_product_qty - 1
