# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import hashlib
from datetime import datetime

from openerp import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    _ESHOP_STATE_SELECTION = [
        ('available', 'Available for Sale'),
        ('disabled', 'Temporarily Disabled'),
        ('unavailable', 'Unavailable for Sale'),
    ]

    eshop_category_id = fields.Many2one(
        comodel_name='eshop.category', string='eShop Category',
        domain=[('type', '=', 'normal')])

    eshop_start_date = fields.Date(string='Start Date of Sale')

    eshop_end_date = fields.Date(string='End Date of Sale')

    eshop_state = fields.Selection(
        string='eShop State', selection=_ESHOP_STATE_SELECTION,
        compute='_compute_eshop_state', store=True)
    # fnct_search=_eshop_state

    eshop_minimum_qty = fields.Float(
        string='Minimum Quantity for eShop', required=True, default=0)

    eshop_rounded_qty = fields.Float(
        string='Rounded Quantity for eShop', required=True, default=0)

    eshop_unpack_qty = fields.Float(
        string='Unpack Quantity for eShop', required=True, default=0)

    eshop_unpack_surcharge = fields.Float(
        string='Unpack Surcharge for eShop', required=True, default=0)

    eshop_description = fields.Text(type='Text', string='Eshop Description')

    eshop_taxes_description = fields.Char(
        compute='eshop_taxes_description', string='Eshop Taxes Description')

    # Compute Section
    @api.multi
    def _compute_eshop_taxes_description(self):
        for product in self:
            product.eshop_taxes_description = ', '.join(
                product.mapped('taxes_id.eshop_description'))

    @api.multi
    def _compute_eshop_state(self):
        for product in self:
            if not (
                    product.eshop_category_id and product.sale_ok and
                    product.active):
                product.eshop_state = 'unavailable'
            else:
                dateNow = datetime.now().strftime('%Y-%m-%d')
                if product.eshop_start_date and product.eshop_end_date:
                    if product.eshop_start_date <= dateNow \
                            and dateNow <= product.eshop_end_date:
                        product.eshop_state = 'available'
                    else:
                        product.eshop_state = 'disabled'
                elif product.eshop_start_date:
                    if product.eshop_start_date <= dateNow:
                        product.eshop_state = 'available'
                    else:
                        product.eshop_state = 'disabled'
                elif product.eshop_end_date:
                    if dateNow <= product.eshop_end_date:
                        product.eshop_state = 'available'
                    else:
                        product.eshop_state = 'disabled'
                else:
                    product.eshop_state = 'available'

    # API eshop Section
    @api.model
    def get_current_eshop_product_list(self, order_id=False):
        """The aim of this function is to deal with delay of response of
        the odoo-eshop, module.
        This will return a list of data, used for catalog inline view."""
        SaleOrder = self.env['sale.order']
        res = []
        line_dict = {}
        # Get current quantities ordered
        if order_id:
            order = SaleOrder.browse(order_id)
            for order_line in order.order_line:
                line_dict[order_line.product_id.id] = {
                    'qty': order_line.product_uom_qty,
                    'discount': order_line.discount,
                }

        company_id = self.env.user.company_id.id

        self.env.cr.execute("""
SELECT
    distinct tmp.*,
    array_to_string(array_agg(label_rel.label_id)
        OVER (PARTITION BY label_rel.product_id), ',') label_ids
FROM (
    SELECT distinct
    pp.id id,
    pt.id as template_id,
    pp.default_code default_code,
    pt.name,
    pt.list_price list_price,
    ec.id category_id,
    ec.sequence category_sequence,
    ec.name category_name,
    ec.complete_name category_complete_name,
    ec.write_date category_write_date,
    pt.uom_id,
    uom.eshop_description uom_eshop_description,
    pp.eshop_minimum_qty,
    pp.eshop_unpack_qty,
    pp.eshop_unpack_surcharge,
    array_to_string(array_agg(tax_rel.tax_id)
        OVER (PARTITION BY tax_rel.prod_id), ',') tax_ids
    FROM product_product pp
    INNER JOIN product_template pt on pt.id = pp.product_tmpl_id
    INNER JOIN eshop_category ec on ec.id = pp.eshop_category_id
    INNER JOIN product_uom uom on uom.id = pt.uom_id
    LEFT OUTER JOIN product_taxes_rel tax_rel ON tax_rel.prod_id = pt.id
    WHERE pt.company_id = %s
    AND pt.sale_ok
    AND pp.active
    AND (eshop_start_date < current_date or eshop_start_date is null)
    AND (current_date < eshop_end_date or eshop_end_date is null)
) as tmp
LEFT OUTER JOIN product_label_product_rel label_rel
    ON label_rel.product_id = tmp.id
order by category_sequence, category_name, name;
""" % company_id)
        columns = self.env.cr.description
        for value in self.env.cr.fetchall():
            product_id = value[0]
            tmp = {}
            for (index, column) in enumerate(value):
                if '_ids' in columns[index][0]:
                    tmp[columns[index][0]] = sorted(
                        [int(x) for x in column.split(',') if x])
                else:
                    tmp[columns[index][0]] = column
            if product_id in line_dict:
                tmp.update({
                    'qty': line_dict[product_id]['qty'],
                    'discount': line_dict[product_id]['discount'],
                })
            else:
                tmp.update({'qty': 0, 'discount': 0})
            if tmp['uom_eshop_description'] is None:
                tmp['uom_eshop_description'] = False
            tmp['category_sha1'] = hashlib.sha1(
                str(tmp['category_write_date'])).hexdigest()
            res.append(tmp)

        return res

    # def _eshop_state(self, cr, uid, obj, name, arg, context=None):
    #     dateNow = datetime.now().strftime('%Y-%m-%d')
    #     if arg[0][1] not in ('=', 'in'):
    #         raise except_orm(
    #             _("The Operator %s is not implemented !") % (arg[0][1]),
    #             str(arg))
    #     if arg[0][1] == '=':
    #         lst = [arg[0][2]]
    #     else:
    #         lst = arg[0][2]
    #     sql_lst = []
    #     if 'available' in lst and len(lst) == 1:
    #         sql_lst.append(
    #             """((
    #                     eshop_start_date is not null
    #                     AND eshop_end_date is not null)
    #                 AND (
    #                     eshop_start_date <= '%s'
    #                     AND '%s' <= eshop_end_date
    #                 )
    #             )""" % (dateNow, dateNow))
    #         sql_lst.append(
    #             """((
    #                     eshop_start_date is null
    #                     AND eshop_end_date is not null)
    #                 AND ('%s' <= eshop_end_date)
    #             )""" % (dateNow))
    #         sql_lst.append(
    #             """((
    #                     eshop_start_date is not null
    #                     AND eshop_end_date is null)
    #                 AND (
    #                     eshop_start_date <= '%s'
    #                 )
    #             )""" % (dateNow))
    #         sql_lst.append(
    #             """(eshop_start_date is null
    #                 AND eshop_end_date is null)""")
    #         for i in range(0, len(sql_lst)):
    #             sql_lst[i] = """(
    #                 eshop_category_id IS NOT NULL
    #                 AND id in (
    #                     SELECT pp.id
    #                     FROM product_product pp
    #                     INNER JOIN product_template pt
    #                         ON pp.product_tmpl_id = pt.id
    #                         AND pt.sale_ok is true)
    #                 AND active is true
    #                 AND (%s))""" % (sql_lst[i])
    #     else:
    #         raise except_orm(
    #             _("This arg %s is not implemented !") % (lst.join(', ')),
    #             str(arg))

    #     where = sql_lst[0]
    #     for item in sql_lst[1:]:
    #         where += " OR %s" % (item)
    #     sql_req = """
    #         SELECT id
    #         FROM product_product
    #         WHERE %s;""" % (where)
    #     cr.execute(sql_req)  # pylint: disable=invalid-commit
    #     res = cr.fetchall()
    #     return [('id', 'in', map(lambda x:x[0], res))]
