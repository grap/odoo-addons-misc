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

from openerp.osv import fields
from . import materialized_model


class pos_sale_category_report(materialized_model.MaterializedModel):
    _name = 'pos.sale.category.report'
    _auto = False
    _log_access = False
    _table_name = 'pos_sale_category_report'

    _LINE_SELECTION = [
        ('invoice', 'Invoice'),
        ('point_of_sale', 'Point Of Sale'),
    ]

    _MONTH_SELECTION = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    _columns = {
        'company_id': fields.many2one(
            'res.company', 'Company', readonly=True, select=1),
        'type': fields.selection(
            _LINE_SELECTION, 'Type', readonly=True),
        'date': fields.date('Date Order', readonly=True),
        'year': fields.char(
            'Year', size=4, readonly=True),
        'month': fields.selection(
            _MONTH_SELECTION, 'Month', readonly=True),
        'day': fields.char(
            'Day', size=128, readonly=True),
        'product_id': fields.many2one(
            'product.product', 'Product', readonly=True),
        'product_active': fields.boolean(
            'Active Product', readonly=True),
        'categ_id_1': fields.many2one(
            'product.category', 'Category of Product', readonly=True),
        'categ_id_2': fields.many2one(
            'product.category', 'Middle Category of Product', readonly=True),
        'categ_id_3': fields.many2one(
            'product.category', 'Root Category of Product', readonly=True),
        'product_uom': fields.many2one(
            'product.uom', 'Unit of Measure', readonly=True),
        'product_uom_qty': fields.float(
            '# of Qty', readonly=True),
        'average_price_vat_excl': fields.float(
            'Average Price VAT Excl.', readonly=True),
        'price_total_vat_excl': fields.float(
            'Total Price VAT Excl.', readonly=True),
        'nbr': fields.integer(
            '# of Lines', readonly=True),
    }

    _materialized_module_name = 'pos_sale_reporting'

    _materialized_sql = """
    SELECT
/* Invoice Not From Point Of Sale And not in 'draft' state ***************** */
        row_number() OVER () AS id,
        lines.company_id,
        lines.type,
        lines.date,
        to_char(lines.date, 'YYYY') as year,
        to_char(lines.date, 'MM') as month,
        to_char(lines.date, 'YYYY-MM-DD') as day,
        lines.product_id,
        lines.product_active,
        lines.categ_id_1,
        pc_parent.id AS categ_id_2,
        pc_parent.parent_id AS categ_id_3,
        lines.product_uom,
        sum(lines.product_uom_qty) AS product_uom_qty,
        sum(lines.price_total_vat_excl) AS price_total_vat_excl,
        CASE WHEN sum(lines.product_uom_qty) != 0 THEN
            (sum(lines.price_total_vat_excl) / sum(lines.product_uom_qty))
        ELSE
            0
        END AS average_price_vat_excl,
        count(*) as nbr
    FROM (
/* Out Invoices not in 'draft / cancel' state ****************************** */
        SELECT
            ai.company_id,
            'invoice' AS type,
            date_trunc('day', ai.date_invoice)::date AS date,
            ail.product_id,
            pp.active as product_active,
            pt.categ_id AS categ_id_1,
            pt.uom_id AS product_uom,
            CASE WHEN ai.type = 'out_invoice' THEN
                ail.quantity / uom_ail.factor * uom_pt.factor
            ELSE
                - (ail.quantity / uom_ail.factor * uom_pt.factor)
            END::decimal(16, 3) as product_uom_qty,
            CASE WHEN ai.type = 'out_invoice' THEN
                ail.price_subtotal
            ELSE
                - (ail.price_subtotal)
            END AS price_total_vat_excl
        FROM account_invoice_line ail
        INNER JOIN account_invoice ai
            ON ail.invoice_id = ai.id
        INNER JOIN product_product pp
            ON ail.product_id = pp.id
        INNER JOIN product_template pt
            ON pp.product_tmpl_id = pt.id
        INNER JOIN product_uom uom_ail
            ON uom_ail.id = ail.uos_id
        INNER JOIN product_uom uom_pt
            ON uom_pt.id = pt.uom_id
        WHERE
            ai.state NOT IN ('draft', 'cancel')
            AND ai.type IN ('out_invoice', 'out_refund')
            AND ail.quantity != 0
            AND ai.id NOT IN (
                SELECT invoice_id
                FROM pos_order
                WHERE invoice_id IS NOT NULL)
    UNION
/* Pos Order not in 'draft' state ****************************************** */
        SELECT
            po.company_id,
            'point_of_sale' AS type,
            date_trunc('day', po.date_order)::date AS date,
            pol.product_id,
            pp.active as product_active,
            pt.categ_id as categ_id_1,
            pt.uom_id as product_uom,
            pol.qty as product_uom_qty,
            pol.price_subtotal as price_total_vat_excl
        FROM pos_order_line pol
        INNER JOIN pos_order po
            ON pol.order_id = po.id
        INNER join product_product pp
            ON pol.product_id = pp.id
        INNER join product_template pt
            ON pp.product_tmpl_id = pt.id
        WHERE
            po.state not IN ('draft')
            AND pol.qty != 0
    ) as lines
INNER JOIN product_category pc
    ON pc.id = categ_id_1
INNER JOIN product_category pc_parent
    ON pc_parent.id = pc.parent_id
GROUP BY
     lines.company_id,
     lines.type,
     lines.date,
     lines.product_id,
     lines.product_active,
     lines.categ_id_1,
     categ_id_2,
     categ_id_3,
     lines.product_uom
"""
