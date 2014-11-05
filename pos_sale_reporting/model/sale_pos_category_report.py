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

from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model


class pos_sale_category_report(Model):
    _name = 'pos.sale.category.report'
    _auto = False
    _table_name = 'pos_sale_category_report'

    _LINE_TYPE = [
        ('invoice', 'Invoice'),
        ('point_of_sale', 'Point Of Sale'),
    ]

    _columns = {
        'company_id': fields.many2one(
            'res.company', 'Company', readonly=True),
        'type': fields.selection(
            _LINE_TYPE, 'Type', readonly=True),
        'date': fields.date('Date Order', readonly=True),
        'product_id': fields.many2one(
            'product.product', 'Product', readonly=True),
        'product_uom': fields.many2one(
            'product.uom', 'Unit of Measure', readonly=True),
        'product_uom_qty': fields.float(
            '# of Qty', readonly=True),
        'categ_id_1': fields.many2one(
            'product.category', 'Category of Product', readonly=True),
        'categ_id_2': fields.many2one(
            'product.category', 'Middle Category of Product', readonly=True),
        'categ_id_3': fields.many2one(
            'product.category', 'Root Category of Product', readonly=True),
        'price_total_vat_excl': fields.float(
            'Total Price VAT Excl.', readonly=True),


#        'year': fields.char('Year', size=4, readonly=True),
#        'month': fields.selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
#            ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
#            ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
#        'day': fields.char('Day', size=128, readonly=True),
#        'delay': fields.float('Commitment Delay', digits=(16,2), readonly=True),
#        'nbr': fields.integer('# of Lines', readonly=True),
#        'state': fields.selection([
#            ('draft', 'Quotation'),
#            ('waiting_date', 'Waiting Schedule'),
#            ('manual', 'Manual In Progress'),
#            ('progress', 'In Progress'),
#            ('invoice_except', 'Invoice Exception'),
#            ('done', 'Done'),
#            ('cancel', 'Cancelled')
#            ], 'Order Status', readonly=True),
#        'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', readonly=True),
#        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', readonly=True),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table_name)
        cr.execute("""
CREATE OR REPLACE VIEW %s AS (
    SELECT
        row_number() OVER () as id, *
    FROM (
        SELECT
            ai.company_id,
            'invoice' as type,
            ai.date_invoice as date,
            ail.product_id,
            pt.categ_id as categ_id_1,
            pc_parent.id as categ_id_2,
            pc_parent.parent_id as categ_id_3,
            pt.uom_id as product_uom,
            CASE WHEN ai.type = 'out_invoice' THEN
                ail.quantity / uom_ail.factor * uom_pt.factor
            ELSE
                - (ail.quantity / uom_ail.factor * uom_pt.factor)
            END::decimal(16, 3) as product_uom_qty,
            CASE WHEN ai.type = 'out_invoice' THEN
                ail.price_subtotal
            ELSE
                - (ail.price_subtotal)
            END as price_total_vat_excl,
            CASE WHEN ail.discount = 100 THEN
                CASE WHEN ai.type = 'out_invoice' THEN
                    ail.price_unit  -- TODO FIXME if vat_include
                ELSE
                    - ail.price_unit -- TODO FIXME if vat_include
                END
            ELSE
                CASE WHEN ai.type = 'out_invoice' THEN
                    ail.price_subtotal * (ail.discount / (100.0 - ail.discount))
                ELSE
                    - (ail.price_subtotal * (ail.discount /
                        (100.0 - ail.discount)))
                END
            END::decimal(16, 2)  as total_discount_vat_excl

        FROM account_invoice_line ail
        INNER JOIN account_invoice ai on ail.invoice_id = ai.id
        LEFT JOIN product_product pp on ail.product_id = pp.id
        INNER JOIN product_template pt on pp.product_tmpl_id = pt.id
        LEFT JOIN product_category pc on pc.id = pt.categ_id
        LEFT JOIN product_category pc_parent on pc_parent.id = pc.parent_id
        LEFT JOIN product_uom uom_ail on uom_ail.id = ail.uos_id
        LEFT JOIN product_uom uom_pt on uom_pt.id = pt.uom_id
        WHERE
        ai.type IN ('out_invoice', 'out_refund')
        AND ail.quantity != 0
        AND ai.id NOT IN (
            SELECT invoice_id
            FROM pos_order
            WHERE invoice_id IS NOT NULL)
    UNION
        SELECT
            po.company_id,
            'point_of_sale' as type,
            po.date_order as date,
            pol.product_id,
            pt.categ_id as categ_id_1,
            pc_parent.id as categ_id_2,
            pc_parent.parent_id as categ_id_3,
            pt.uom_id as product_uom,
            pol.qty as product_uom_qty,
            pol.price_subtotal as price_total_vat_excl,
                CASE WHEN pol.discount = 100 THEN
                    pol.price_unit  -- TODO FIXME if vat_include
                ELSE
                    pol.price_subtotal * (pol.discount /
                        (100.0 - pol.discount))
                END::decimal(16, 2)  as total_discount_vat_excl
        FROM pos_order_line pol
        INNER JOIN pos_order po on pol.order_id = po.id
        INNER join product_product pp on pol.product_id = pp.id
        INNER join product_template pt on pp.product_tmpl_id = pt.id
        INNER join product_category pc on pc.id = pt.categ_id
        INNER join product_category pc_parent on pc_parent.id = pc.parent_id
    ) as lines
)""" % (self._table_name))
