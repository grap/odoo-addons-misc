# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class AccountJournal(orm.Model):
    _inherit = 'account.journal'

    _columns = {
        'is_default_quick_payment': fields.boolean(
            'By Default for Quick Payment'),
    }
