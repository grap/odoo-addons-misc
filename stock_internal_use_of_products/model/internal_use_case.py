# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock - Internal Use Of Products for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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


class internal_use_case(Model):
    _name = "internal.use.case"
    _description = "Case of Internal Uses"

    # Columns Section
    _columns = {
        'name': fields.char('Name', size=64, required=True,),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'location_from': fields.many2one(
            'stock.location', 'Origin Location', required=True,
            domain="[('usage','=','internal')]"),
        'location_to': fields.many2one(
            'stock.location', 'Destination Location', required=True),
        'expense_account': fields.property(
            'account.account',
            type='many2one',
            relation='account.account',
            string="Expense Account",
            view_load=True,
            required=True),
        'active': fields.boolean(
            'Active', help="""By unchecking the active field, you may hide"""
            """ an INCOTERM without deleting it."""),
        'journal': fields.many2one(
            'account.journal', 'Journal', required=True),
    }

    # Defaults section
    _defaults = {
        'company_id': (
            lambda s, cr, uid, c: s.pool.get('res.users')._get_company(
                cr, uid, context=c)),
        'active': True,
    }

    # Constraints Section
    def _check_company_id(self, cr, uid, ids, context=None):
        for iuc in self.browse(cr, uid, ids, context=context):
            if (iuc.company_id.id != iuc.location_from.company_id.id or
                    iuc.company_id.id != iuc.location_to.company_id.id):
                return False
        return True

    def _check_different_location_ids(self, cr, uid, ids, context=None):
        for iuc in self.browse(cr, uid, ids, context=context):
            if iuc.location_from.id == iuc.location_to.id:
                return False
        return True

    def _check_location_usages(self, cr, uid, ids, context=None):
        for iuc in self.browse(cr, uid, ids, context=context):
            if (iuc.location_from.usage == 'view' or
                    iuc.location_to.usage == 'view'):
                return False
        return True

    _constraints = [
        (
            _check_company_id,
            """Error: Origin location and Destination Location must belong"""
            """ to the company.""",
            ['location_from', 'location_to', 'company_id']),
        (
            _check_different_location_ids,
            """Error: Origin location and Destination Location must be"""
            """ different.""",
            ['location_from', 'location_to']),
        (
            _check_location_usages,
            """Error: Origin location and Destination Location can not be"""
            """ of 'view' type.""",
            ['location_from', 'location_to']),
    ]

    _sql_constraints = [(
        'name_company_id_uniq',
        'unique(name,company_id)',
        'Case of Internal uses name must be unique by company!')]

    # Overload Section
    def copy_data(self, cr, uid, record_id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'name': '%s (copy)' % (self.browse(
                cr, uid, record_id, context=context).name)
        })
        return super(internal_use_case, self).copy_data(
            cr, uid, record_id, default, context=context)
