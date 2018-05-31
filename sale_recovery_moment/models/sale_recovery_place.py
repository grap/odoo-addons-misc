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


class sale_recovery_place(Model):
    _description = 'Recovery Place'
    _name = 'sale.recovery.place'
    _order = 'name'

    # Field Functions Section
    def _get_complete_name(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for srp in self.browse(cr, uid, ids, context):
            address_format = srp.country_id \
                and srp.country_id.address_format \
                or "%(street)s\n%(street2)s\n%(city)s %(state_code)s" \
                " %(zip)s\n%(country_name)s"
            args = {
                'street': srp.street and srp.street or '',
                'street2': srp.street2 and srp.street2 or '',
                'zip': srp.zip and srp.zip or '',
                'city': srp.city and srp.city or '',
                'state_code': srp.state_id and srp.state_id.code or '',
                'state_name': srp.state_id and srp.state_id.name or '',
                'country_code': srp.country_id and srp.country_id.code or '',
                'country_name': srp.country_id and srp.country_id.name or '',
            }
            res[srp.id] = srp.name + ' - ' \
                + (address_format % args).replace('\n', ' ')
        return res

    # Column Section
    _columns = {
        'name': fields.char(
            'Name', required=True),
        'complete_name': fields.function(
            _get_complete_name, type='char', string='Name',
            select=True, store={
                'sale.recovery.place': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'name', 'street', 'street2', 'zip', 'city', 'state_id',
                        'country_id'], 10)}),
        'company_id': fields.many2one(
            'res.company', string='Company', required=True),
        'active': fields.boolean('Active'),
        'street': fields.char('Street'),
        'street2': fields.char('Street2'),
        'zip': fields.char('ZIP', change_default=True, size=24),
        'city': fields.char('City'),
        'state_id': fields.many2one('res.country.state', 'State'),
        'country_id': fields.many2one('res.country', 'Country'),
    }

    _defaults = {
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
        'active': True,
    }

    # View Section
    def onchange_state_id(self, cr, uid, ids, state_id, context=None):
        if state_id:
            country_id = self.pool.get('res.country.state').browse(
                cr, uid, state_id, context).country_id.id
            return {'value': {'country_id': country_id}}
        return {}
