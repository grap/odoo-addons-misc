# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale - Reporting for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
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

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp import tools


class pos_daily_simple_report(Model):
    _name = 'pos.daily.simple.report'
    _auto = False
    _table = 'pos_daily_simple_report'

    _columns = {
        'date': fields.date('Date'),
        'date_string': fields.char('Date', size=64, required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'amount_tax_excluded': fields.float('Net Sales', digits=(12, 2)),
        'nb_orders': fields.integer('Nb of orders'),
        'avg_amount': fields.float('Average amount', digits=(12, 2)),
    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            create or replace view %s as (
                SELECT
                    a.id,
                    a.date,
                    a.date_string,
                    a.company_id,
                    b.amount_tax_excluded,
                    a.nb_orders,
                    b.amount_tax_excluded / a.nb_orders as avg_amount
                FROM
                    (
                    SELECT
                        min(id) as id,
                        date_trunc('day',date_order) as date,
                        to_char(date_order,'YY/MM/DD Dy') as date_string,
                        company_id AS company_id,
                        count(*) as nb_orders
                    FROM
                        pos_order po
                    WHERE
                        po.state not in ('draft')
                        AND date_order > now() - 3 * interval '1 month'
                    GROUP BY
                        company_id,
                        date,
                        date_string
                    ) as a
                INNER JOIN
                    (
                    SELECT
                        po.company_id,
                        date_trunc('day',po.date_order) as date,
                        round(sum(pol.price_subtotal),2) as amount_tax_excluded
                    FROM
                        pos_order po
                        INNER JOIN pos_order_line pol
                            ON po.id = pol.order_id
                    WHERE
                        po.state not in ('draft')
                        AND po.date_order > now() - 3 * interval '1 month'
                    GROUP BY
                        po.company_id,
                        date_trunc('day',po.date_order)
                    ) as b
                ON a.date = b.date AND a.company_id=b.company_id
        )""" % (self._table))
