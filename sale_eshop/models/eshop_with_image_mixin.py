# coding: utf-8
# Copyright (C) 2014-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp import api, fields, models


class EshopWithImageMixin(models.AbstractModel):
    _name = 'eshop.with.image.mixin'
    _inherit = 'eshop.mixin'

    _eshop_image_fields = []

    image_write_date = fields.Datetime(
        readonly=True, required=True,
        default=lambda s: s._default_image_write_date())

    @api.model
    def _default_image_write_date(self):
        return self._get_image_write_date()

    @api.model
    def _get_image_write_date(self):
        return datetime.now()

    @api.model
    def create(self, vals):
        vals.update({'image_write_date': self._get_image_write_date()})
        return super(EshopWithImageMixin, self).create(vals)

    @api.multi
    def _write_eshop_invalidate(self, vals):
        if list(set(self._eshop_image_fields) & set(vals.keys())):
            vals.update({'image_write_date': self._get_image_write_date()})
        return super(EshopWithImageMixin, self)._write_eshop_invalidate(vals)

    # Overload section
    @api.model
    def _get_eshop_fields(self):
        fields = super(EshopWithImageMixin, self)._get_eshop_fields()
        for field in fields:
            if 'image' in field:
                fields.remove(field)
        fields.append('image_write_date')
        return fields
