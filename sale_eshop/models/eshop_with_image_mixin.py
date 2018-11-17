# coding: utf-8
# Copyright (C) 2014-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp import api, fields, models


class EshopWithImageMixin(models.AbstractModel):
    _name = 'eshop.with.image.mixin'
    _inherit = 'eshop.mixin'

    image_write_date = fields.Datetime(
        commpute='_compute_image_write_date', store=True)

    @api.multi
    @api.depends('image')
    def _compute_image_write_date(self):
        today = datetime.now()
        for item in self:
            item.image_write_date = today

    # Overload section
    @api.model
    def _get_eshop_fields(self):
        fields = super(EshopWithImageMixin, self)._get_eshop_fields()
        for field in fields:
            if 'image' in field:
                fields.remove(field)
        fields.append('image_write_date')
        return fields
