# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - eShop for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

from datetime import datetime

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp.osv.orm import except_orm
from openerp.tools.translate import _

from openerp.addons.sale_eshop import demo_image


class ProductProduct(Model):
    _inherit = 'product.product'

    _ESHOP_STATE_SELECTION = [
        ('available', 'Available for Sale'),
        ('disabled', 'Temporarily Disabled'),
        ('unavailable', 'Unavailable for Sale'),
    ]

    def _eshop_state(self, cr, uid, obj, name, arg, context=None):
        dateNow = datetime.now().strftime('%Y-%m-%d')
        if arg[0][1] not in ('=', 'in'):
            raise except_orm(
                _("The Operator %s is not implemented !") % (arg[0][1]),
                str(arg))
        if arg[0][1] == '=':
            lst = [arg[0][2]]
        else:
            lst = arg[0][2]
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
            raise except_orm(
                _("This arg %s is not implemented !") % (lst.join(', ')),
                str(arg))

        where = sql_lst[0]
        for item in sql_lst[1:]:
            where += " OR %s" % (item)
        sql_req = """
            SELECT id
            FROM product_product
            WHERE %s;""" % (where)
        cr.execute(sql_req)
        res = cr.fetchall()
        return [('id', 'in', map(lambda x:x[0], res))]

    # Field function Section
    def _get_eshop_taxes_description(
            self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context=context):
            if pp.taxes_id:
                res[pp.id] = ', '.join(
                    [x.eshop_description for x in pp.taxes_id])
            else:
                res[pp.id] = ''
        return res

    def _get_eshop_state(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context=context):
            if not (pp.eshop_category_id and pp.sale_ok and pp.active):
                res[pp.id] = 'unavailable'
            else:
                dateNow = datetime.now().strftime('%Y-%m-%d')
                if pp.eshop_start_date and pp.eshop_end_date:
                    if pp.eshop_start_date <= dateNow \
                            and dateNow <= pp.eshop_end_date:
                        res[pp.id] = 'available'
                    else:
                        res[pp.id] = 'disabled'
                elif pp.eshop_start_date:
                    if pp.eshop_start_date <= dateNow:
                        res[pp.id] = 'available'
                    else:
                        res[pp.id] = 'disabled'
                elif pp.eshop_end_date:
                    if dateNow <= pp.eshop_end_date:
                        res[pp.id] = 'available'
                    else:
                        res[pp.id] = 'disabled'
                else:
                    res[pp.id] = 'available'
        return res

    # Columns Section
    _columns = {
        'eshop_category_id': fields.many2one(
            'eshop.category', 'eShop Category', domain=[
                ('type', '=', 'normal')]),
        'eshop_start_date': fields.date(
            'Start Date of Sale'),
        'eshop_end_date': fields.date(
            'End Date of Sale'),
        'eshop_state': fields.function(
            _get_eshop_state, type='selection', string='eShop State',
            fnct_search=_eshop_state, selection=_ESHOP_STATE_SELECTION),
        'eshop_minimum_qty': fields.float(
            'Minimum Quantity for eShop', required=True),
        'eshop_rounded_qty': fields.float(
            'Rounded Quantity for eShop', required=True),
        'eshop_unpack_qty': fields.float(
            'Unpack Quantity for eShop', required=True),
        'eshop_unpack_surcharge': fields.float(
            'Unpack Surcharge for eShop', required=True),
        'eshop_taxes_description': fields.function(
            _get_eshop_taxes_description, type='char',
            string='Eshop Taxes Description'),
        'eshop_description': fields.text(
            type='Text', string='Eshop Description'),
    }

    # Defaults Section
    _defaults = {
        'eshop_minimum_qty': 0,
        'eshop_rounded_qty': 0,
        'eshop_unpack_qty': 0,
        'eshop_unpack_surcharge': 0,
    }

    # Demo Function Section
    def _demo_init_image(self, cr, uid, ids=None, context=None):
        demo_image.init_image(
            self.pool, cr, uid, 'product.product', 'image',
            '/static/src/img/demo/product_product/', context=context)

    # Custom Section
    def get_current_eshop_product_list(self, cr, uid, order_id, context=None):
        """The aim of this function is to deal with delay of response of
        the odoo-eshop, module.
        This will return a list of data, used for catalog inline view."""
        so_obj = self.pool['sale.order']
        ru_obj = self.pool['res.users']
        res = []
        line_dict = {}
        # Get current quantities ordered
        if order_id:
            so = so_obj.browse(cr, uid, order_id, context=context)
            for sol in so.order_line:
                line_dict[sol.product_id.id] = {
                    'qty': sol.product_uom_qty,
                    'discount': sol.discount,
                }

        company_id = ru_obj.browse(cr, uid, uid, context=context).company_id.id
        cr.execute("""
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
    pp.delivery_categ_id,
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
        columns = cr.description
        for value in cr.fetchall():
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
            if tmp['delivery_categ_id'] is None:
                tmp['delivery_categ_id'] = False
            res.append(tmp)

        return res
