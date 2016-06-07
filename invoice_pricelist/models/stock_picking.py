# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Prepare Section
    @api.model
    def _prepare_invoice(self, picking, partner, inv_type, journal_id):
        res = super(StockPicking, self)._prepare_invoice(
            picking, partner, inv_type, journal_id)
        if picking.sale_id:
            res['pricelist_id'] = picking.sale_id.pricelist_id.id
        elif picking.purchase_id:
            res['pricelist_id'] = picking.purchase_id.pricelist_id.id
        # Otherwise, create function of invoice model will set default partner
        # pricelist
        return res
