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
    }

    # Defaults Section
    _defaults = {
        'eshop_minimum_qty': 1,
        'eshop_rounded_qty': 1,
    }

    # Demo Function Section
    def _demo_init_image(self, cr, uid, ids=None, context=None):
        demo_image.init_image(
            self.pool, cr, uid, 'product.product', 'image',
            '/static/src/img/demo/product_product/', context=context)
