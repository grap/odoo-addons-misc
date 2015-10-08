# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recovery Moment Module for Odoo
#    Copyright (C) 2014 - Today GRAP (http://www.grap.coop)
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


class SaleDeliveryCategory(Model):
    _name = 'sale.delivery.category'
    _order = 'name'

    # Column Section
    _columns = {
        'name': fields.char(
            'Name', required=True),
        'partner_ids': fields.one2many(
            'res.partner', 'delivery_categ_id', string='Partners'),
        'company_id': fields.many2one(
            'res.company', string='Company', required=True),
        'active': fields.boolean('Active'),
        'moment_ids': fields.one2many(
            'sale.delivery.moment', 'delivery_categ_id', string='Moments'),
    }

    _defaults = {
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
        'active': True,
    }
