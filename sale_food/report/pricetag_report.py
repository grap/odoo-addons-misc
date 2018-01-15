# -*- coding: utf-8 -*-
import time
from openerp.addons.report_webkit import webkit_report
from openerp.report import report_sxw


class report_webkit_html(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_webkit_html, self).__init__(
            cr, uid, name, context=context)
        # updating product to update edition_state to the value 'OK'
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

webkit_report.WebKitParser(
    'report.pricetag.report',
    'product.pricetag.wizard',
    'addons/sale_food/report/pricetag_report.mako',
    parser=report_webkit_html)


report_sxw.report_sxw(
    'report.pricetag.report.tall',
    'product.pricetag.wizard',
    'addons/sale_food/report/pricetag_report_tall.mako',
    parser=report_webkit_html)

report_sxw.report_sxw(
    'report.pricetag.report.small',
    'product.pricetag.wizard',
    'addons/sale_food/report/pricetag_report_small.mako',
    parser=report_webkit_html)
