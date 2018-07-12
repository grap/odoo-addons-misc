# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class AccountInvoice(Model):
    _inherit = 'account.invoice'

    # Columns section
    _columns = {
        'forbid_payment': fields.boolean(
            'Forbid Payment', help="""Indicates an invoice where no payment"""
            """ should be registered. eg: invoice from POS are already"""
            """ paid."""),
    }
