# -*- coding: utf-8 -*-
import time
from report import report_sxw


class report_pricetag(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        sql_req = """
            UPDATE product_product
            SET pricetag_state=0
            WHERE id in (
                SELECT product_id
                FROM product_pricetag_wizard_line
                WHERE wizard_id = %s)"""
        cr.execute(sql_req % (context['active_id']))
        super(report_pricetag, self).__init__(cr, uid, name, context=context)
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
