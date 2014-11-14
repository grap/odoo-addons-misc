# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Food Module for Odoo
#    Copyright (C) 2012-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.report import report_sxw


class report_pricetag(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_pricetag, self).__init__(cr, uid, name, context=context)
        sql_req = """
            UPDATE product_product
            SET pricetag_state=0
            WHERE id in (
                SELECT product_id
                FROM product_pricetag_wizard_line
                WHERE wizard_id = %s)"""
        cr.execute(sql_req % (context['active_id']))
        self.localcontext.update({
            'time': time,
            'cr': cr,
            'uid': uid,
        })

report_sxw.report_sxw(
    'report.pricetag',
    'product.pricetag.wizard',
    'addons/sale_food/view/report_pricetag.mako',
    parser=report_pricetag)
