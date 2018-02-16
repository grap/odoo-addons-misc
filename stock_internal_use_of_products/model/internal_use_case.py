# coding: utf-8
# Copyright (C) 2013-Today GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class InternalUseCase(models.Model):
    _name = 'internal.use.case'

    # Default Section
    def _default_company_id(self):
        return self.env.user.company_id

    # Columns Section
    name = fields.char(string='Name', required=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', required=True,
        select=True, default=_default_company_id)

    active = fields.Boolean(
        string='Active', default=True, help="By unchecking the active field,"
        " you may hide an Use Case without deleting it.")

    default_location_src_id = fields.Many2one(
        comodel_name='stock.location', string='Origin Location', required=True,
        domain="[('usage','=','internal')]", old_name='location_from')

    default_location_dest_id = fields.many2one(
        comodel_name'stock.location', string='Destination Location',
        required=True, old_name='location_to')

    journal_id = fields.many2one(
        comodel_name='account.journal', string='Journal', required=True,
        help="Set the Accounting Journal used to generate Accounting Entries",
        old_name='journal')

    account_id = fields.Many2one(
        comodel_name'account.account', string='Expense Account', required=True,
        domain="[('type','=','other')]", old_name='expense_account',
        help="Expense account of the Use Case. The generated"
        " Entries will belong the following lines:\n\n"
        " * Debit: This Expense Account;"
        " * Credit: The Default Expense Account of the Product;")

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


    @api.multi
    def copy_data(self, default=None):
        default = default and default or {}
        default['name'] = _('%s (copy)') % self.name
        return super(InternalUseCase, self).copy_data(default)
