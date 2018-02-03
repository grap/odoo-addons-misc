# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, tools


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    image = fields.Binary(string='Image')

    image_medium = fields.Binary(
        string='Medium-sized image', compute='_compute_multi_image',
        inverse='_set_image_medium')

    image_small = fields.Binary(
        string='Small-sized image', compute='_compute_multi_image',
        inverse='_set_image_small')

    @api.depends('image')
    def _compute_multi_image(self):
        for picking_type in self:
            res = tools.image_get_resized_images(
                picking_type.image, avoid_resize_medium=True)
            picking_type.write({
               'image_medium': res['image_medium'],
               'image_small': res['image_small'],
            })

    @api.multi
    def _set_image_medium(self):
        for picking_type in self:
            picking_type.image = self.image_medium

    @api.multi
    def _set_image_small(self):
        for picking_type in self:
            picking_type.image = self.image_small
