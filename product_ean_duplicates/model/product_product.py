# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - EAN Duplicates Module for Odoo
#    Copyright (C) 2014 -Today GRAP (http://www.grap.coop)
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
from openerp.osv.orm import Model


class product_product(Model):
    _inherit = 'product.product'

    def _search_ean_duplicates_exist(
            self, cr, uid, obj, name, arg, context=None):
        pp_ids = self.search(cr, uid, [], context=context)
        tmp = self._get_ean_duplicates(
            cr, uid, pp_ids, None, None, context=context)
        res = []
        for k, v in tmp.items():
            if v['ean_duplicates_exist'] == arg[0][2]:
                res.append(k)
        return [('id', 'in', res)]

    def _get_ean_duplicates(self, cr, uid, ids, name, args, context=None):
        res = {x: {
            'ean_duplicates_exist': False,
            'ean_duplicates_qty': 0,
        } for x in ids}
        sql_req = """
            SELECT
                pp1.id,
                count(*) as qty
            FROM product_product pp1
            INNER JOIN product_template pt1
                ON pt1.id = pp1.product_tmpl_id
            INNER JOIN product_product pp2
                ON pp1.ean13 = pp2.ean13
                AND pp1.id != pp2.id
                AND pp2.active = True
            INNER JOIN product_template pt2
                ON pt2.id = pp2.product_tmpl_id
                AND pt1.company_id = pt2.company_id
            WHERE
                pp1.ean13 IS NOT NULL
                AND pp1.ean13 != ''
                AND pp1.id in (%s)
            GROUP BY pp1.id
            ORDER BY pp1.id""" % (', '.join([str(id) for id in ids]))
        cr.execute(sql_req)
        tmp = cr.fetchall()
        for item in tmp:
            res[item[0]]['ean_duplicates_qty'] = item[1]
            res[item[0]]['ean_duplicates_exist'] = True
        return res

    _columns = {
        'ean_duplicates_exist': fields.function(
            _get_ean_duplicates, type='boolean',
            string='Has EAN Duplicates', multi=_get_ean_duplicates,
            fnct_search=_search_ean_duplicates_exist),
        'ean_duplicates_qty': fields.function(
            _get_ean_duplicates, type='integer',
            string='EAN Duplicates Quantity', multi=_get_ean_duplicates),
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default['ean13'] = ''
        return super(product_product, self).copy(
            cr, uid, id, default, context=context)
