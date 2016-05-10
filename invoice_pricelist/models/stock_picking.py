# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class StockPicking(Model):
    _inherit = 'stock.picking'

    # Prepare Section
    def _prepare_invoice(
            self, cr, uid, picking, partner, inv_type, journal_id,
            context=None):
        res = super(StockPicking, self)._prepare_invoice(
            cr, uid, picking, partner, inv_type, journal_id, context=context)
        if picking.sale_id:
            res['pricelist_id'] = picking.sale_id.pricelist_id.id
        elif picking.purchase_id:
            res['pricelist_id'] = picking.purchase_id.pricelist_id.id
        # Otherwise, create function of invoice model will set default partner
        # pricelist
        return res
