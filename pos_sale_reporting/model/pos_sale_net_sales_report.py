# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale / Sale Reporting module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

from openerp import SUPERUSER_ID, tools
from openerp.osv import fields
from . import materialized_model


class pos_sale_net_sales_report(materialized_model.MaterializedModel):
    _name = 'pos.sale.net.sales.report'
    _auto = False
    _table_name = 'pos_sale_net_sales_report'

    _LINE_TYPE = [
        ('01_invoice_sale', 'Invoice - Via Sale'),
        ('02_invoice_pos', 'Invoice - Via Point Of Sale'),
        ('03_pos_normal', 'Point of Sale - Normal'),
    ]

    def init(self, cr):
        imm_obj = self.pool['ir.module.module']
        imm_id = imm_obj.search(cr, SUPERUSER_ID, [
            ('name', '=', 'pos_sale_reporting'),
            ('state', '=', 'to install')])
        if len(imm_id) != 0:
            tools.drop_view_if_exists(cr, 'pos_sale_month_date')
            cr.execute("""
            CREATE VIEW pos_sale_month_date AS (
                SELECT month_date, company_id, partner_id, pricelist_id
                FROM (
                    SELECT
                        date(date_trunc('month', date_order)) AS month_date,
                        company_id,
                        coalesce (partner_id, 0) as partner_id,
                        pricelist_id
                    FROM pos_order
                    WHERE state in ('paid', 'done')
                    GROUP BY month_date, company_id, partner_id, pricelist_id
                UNION
                    SELECT
                        date(date_trunc('month', date_invoice)) AS month_date,
                        company_id,
                        partner_id,
                        partner_pricelist_id as pricelist_id
                    FROM account_invoice
                    WHERE date_invoice IS NOT NULL
                    AND type IN ('out_invoice', 'out_refund')
                    AND state NOT IN ('draft', 'cancel')
                    GROUP BY
                        month_date,company_id,
                        partner_id,
                        partner_pricelist_id
                ) AS month_temp
                GROUP BY month_date, company_id, partner_id, pricelist_id
            )""")
        super(pos_sale_net_sales_report, self).init(cr)

    _columns = {
        'month_date': fields.date(
            'Month Date', readonly=True),
        'company_id': fields.many2one(
            'res.company', 'Company', readonly=True),
        'partner_id': fields.many2one(
            'res.partner', 'Partner', readonly=True),
        'pricelist_id': fields.many2one(
            'product.pricelist', 'Pricelist', readonly=True),
        'line_type': fields.selection(
            _LINE_TYPE, 'Type', readonly=True),
        'total': fields.float(
            'Total', digits=(16, 2), readonly=True),
    }

    _materialized_module_name = 'pos_sale_reporting'

    _materialized_sql = """
    SELECT
        row_number() OVER () as id,
        month_date,
        company_id,
        CASE
            WHEN (partner_id = 0) THEN null
            ELSE partner_id
        END,
        pricelist_id,
        line_type,
        total
    FROM (
/* Paid / Done Pos Order *************************************************** */
        SELECT
            pos_sale_month_date.month_date,
            pos_sale_month_date.company_id,
            pos_sale_month_date.partner_id,
            pos_sale_month_date.pricelist_id,
            '03_pos_normal' AS line_type,
            COALESCE(result.total, 0) AS total
        FROM pos_sale_month_date
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_order)) AS month_date,
                coalesce(partner_id, 0) as partner_id,
                pricelist_id,
                sum(total) AS total
            FROM pos_order po
            INNER JOIN (
                SELECT
                    order_id,
                    sum(price_subtotal) AS total
                FROM pos_order_line
                GROUP BY order_id
            ) pol
            ON po.id = pol.order_id
            WHERE state in ('paid', 'done')
            GROUP BY company_id, month_date, partner_id, pricelist_id
        ) as result
        ON result.company_id = pos_sale_month_date.company_id
        AND result.month_date = pos_sale_month_date.month_date
        AND result.partner_id = pos_sale_month_date.partner_id
        AND result.pricelist_id = pos_sale_month_date.pricelist_id

/* Invoice from Point Of Sale Module ************************************** */
    UNION
        SELECT
            pos_sale_month_date.month_date,
            pos_sale_month_date.company_id,
            pos_sale_month_date.partner_id,
            pos_sale_month_date.pricelist_id,
            '02_invoice_pos' AS line_type,
            COALESCE(total_out_invoice, 0)
                - COALESCE(total_out_refund, 0) AS total
        FROM pos_sale_month_date
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                partner_id,
                partner_pricelist_id as pricelist_id,
                sum(amount_untaxed) total_out_invoice
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_invoice')
                AND id IN (
                    SELECT invoice_id
                    FROM pos_order
                    WHERE invoice_id IS NOT NULL)
                AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date, partner_id, partner_pricelist_id
            ) AS result_invoice
            ON result_invoice.company_id = pos_sale_month_date.company_id
            AND result_invoice.month_date = pos_sale_month_date.month_date
            AND result_invoice.partner_id = pos_sale_month_date.partner_id
            AND result_invoice.pricelist_id = pos_sale_month_date.pricelist_id
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                partner_id,
                partner_pricelist_id pricelist_id,
                sum(amount_untaxed) total_out_refund
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_refund')
                AND id IN (
                    SELECT invoice_id
                    FROM pos_order
                    WHERE invoice_id IS NOT NULL)
            AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date, partner_id, partner_pricelist_id
            ) AS result_refund
            ON result_invoice.company_id = pos_sale_month_date.company_id
            AND result_invoice.month_date = pos_sale_month_date.month_date
            AND result_invoice.partner_id = pos_sale_month_date.partner_id
            AND result_invoice.pricelist_id = pos_sale_month_date.pricelist_id

/* Invoice from Sale Module ********************************************** */
    UNION
        SELECT
            pos_sale_month_date.month_date,
            pos_sale_month_date.company_id,
            pos_sale_month_date.partner_id,
            pos_sale_month_date.pricelist_id,
            '01_invoice_sale' AS line_type,
            COALESCE(total_out_invoice, 0)
                - COALESCE(total_out_refund, 0) AS total
        FROM pos_sale_month_date
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                partner_id,
                partner_pricelist_id as pricelist_id,
                sum(amount_untaxed) total_out_invoice
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_invoice')
                AND id NOT IN (
                    SELECT invoice_id
                    FROM pos_order
                    WHERE invoice_id IS NOT NULL)
                AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date, partner_id, partner_pricelist_id
            ) AS result_invoice
            ON result_invoice.company_id = pos_sale_month_date.company_id
            AND result_invoice.month_date = pos_sale_month_date.month_date
            AND result_invoice.partner_id = pos_sale_month_date.partner_id
            AND result_invoice.pricelist_id = pos_sale_month_date.pricelist_id
        LEFT JOIN (
            SELECT
                company_id,
                date(date_trunc('month', date_invoice)) month_date,
                partner_id,
                partner_pricelist_id as pricelist_id,
                sum(amount_untaxed) total_out_refund
            FROM account_invoice
            WHERE
                state NOT IN ('draft', 'cancel')
                AND type IN ('out_refund')
                AND id NOT IN (
                SELECT invoice_id
                FROM pos_order
                WHERE invoice_id IS NOT NULL)
            AND date_invoice IS NOT NULL
            GROUP BY company_id, month_date, partner_id, pricelist_id
            ) AS result_refund
            ON result_refund.company_id = pos_sale_month_date.company_id
            AND result_refund.month_date = pos_sale_month_date.month_date
            AND result_refund.partner_id = pos_sale_month_date.partner_id
            AND result_refund.pricelist_id = pos_sale_month_date.pricelist_id

    ) as result_tmp
    ORDER BY month_date, company_id, partner_id, pricelist_id

"""
