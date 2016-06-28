# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields

import openerp.addons.decimal_precision as dp


class StockPickingQuickInvoiceLineWizard(orm.TransientModel):
    _name = 'stock.picking.quick.invoice.line.wizard'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'stock.picking.quick.invoice.wizard', 'Wizard', select=True),
        'journal_id': fields.many2one(
            'account.journal', 'Payment Method', required=True,
            domain="[('type', 'in', ['bank', 'cash'])]"),
        'amount': fields.float(
            digits_compute=dp.get_precision('Account'), string='Amount',
            required=True),
    }
