# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'eshop.with.image.mixin']

    # Inherit Section
    _eshop_invalidation_type = 'single'

    _eshop_invalidation_fields = [
        'name', 'uom_id', 'image', 'image_medium', 'list_price',
        'eshop_category_id', 'label_ids', 'eshop_minimum_qty',
        'eshop_rounded_qty', 'origin_description', 'maker_description',
        'fresh_category', 'eshop_description', 'country_id',
        'department_id', 'default_code',
        'eshop_taxes_description', 'eshop_unpack_qty',
        'eshop_unpack_surcharge',
    ]

    _eshop_image_fields = ['image', 'image_medium', 'image_small']

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
        compute='_compute_eshop_state', search='_search_eshop_state')

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
        compute='_compute_eshop_taxes_description',
        string='Eshop Taxes Description')

    # Compute Section
    @api.multi
    @api.depends('taxes_id.eshop_description')
    def _compute_eshop_taxes_description(self):
        for product in self:
            product.eshop_taxes_description = ', '.join(
                product.mapped('taxes_id.eshop_description'))

    @api.multi
    @api.depends(
        'eshop_category_id', 'sale_ok', 'active', 'eshop_start_date',
        'eshop_end_date')
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

    # Overload Section
    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        self._write_eshop_invalidate(vals)
        return super(ProductProduct, self).write(vals)

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

        req = """
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
    ec.image_write_date category_image_write_date,
    ec.image_write_date_hash category_image_write_date_hash,
    pp.image_write_date product_image_write_date,
    pp.image_write_date_hash product_image_write_date_hash,
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
""" % company_id  # pylint: disable=sql-injection
        self.env.cr.execute(req)
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
            if tmp['default_code'] is None:
                tmp['default_code'] = False

            res.append(tmp)

        return res

    def _search_eshop_state(self, operator, value):
        dateNow = datetime.now().strftime('%Y-%m-%d')
        if operator not in ('=', 'in'):
            raise UserError(_(
                "The Operator %s is not implemented !" % (operator)))
        if operator == '=':
            lst = [value]
        else:
            lst = value
        sql_lst = []
        if 'available' in lst and len(lst) == 1:
            sql_lst.append(
                """((
                        eshop_start_date is not null
                        AND eshop_end_date is not null)
                    AND (
                        eshop_start_date <= '%s'
                        AND '%s' <= eshop_end_date
                    )
                )""" % (dateNow, dateNow))
            sql_lst.append(
                """((
                        eshop_start_date is null
                        AND eshop_end_date is not null)
                    AND ('%s' <= eshop_end_date)
                )""" % (dateNow))
            sql_lst.append(
                """((
                        eshop_start_date is not null
                        AND eshop_end_date is null)
                    AND (
                        eshop_start_date <= '%s'
                    )
                )""" % (dateNow))
            sql_lst.append(
                """(eshop_start_date is null
                    AND eshop_end_date is null)""")
            for i in range(0, len(sql_lst)):
                sql_lst[i] = """(
                    eshop_category_id IS NOT NULL
                    AND id in (
                        SELECT pp.id
                        FROM product_product pp
                        INNER JOIN product_template pt
                            ON pp.product_tmpl_id = pt.id
                            AND pt.sale_ok is true)
                    AND active is true
                    AND (%s))""" % (sql_lst[i])
        else:
            raise UserError(_(
                "This arg %s is not implemented !" % (value)))

        where = sql_lst[0]
        for item in sql_lst[1:]:
            where += " OR %s" % (item)
        sql_req = """
            SELECT id
            FROM product_product
            WHERE %s;""" % (where)  # pylint: disable=sql-injection
        self.env.cr.execute(sql_req)
        res = self.env.cr.fetchall()
        return [('id', 'in', map(lambda x:x[0], res))]

    # Overwrite section
    @api.model
    def _get_eshop_domain(self):
        return [('eshop_state', '=', 'available')]
