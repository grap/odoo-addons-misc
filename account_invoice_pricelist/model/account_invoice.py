# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Price List on Invoice for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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

from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.osv.orm import Model
from openerp.tools.translate import _


class account_invoice(Model):
    _inherit = 'account.invoice'

    def _get_partner_pricelist_id(
            self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context == {}:
            # Init, when installing the module
            results = self.read(cr, uid, ids, ['company_id'])
            for result in results:
                context['force_company'] = result['company_id'][0]
                ai = self.browse(cr, uid, result['id'], context=context)
                if ai.type in ('out_invoice', 'out_refund'):
                    res[ai.id] =\
                        ai.partner_id.property_product_pricelist.id
                elif ai.type in ('in_invoice', 'in_refund'):
                    if ai.partner_id._model._columns.get(
                            'property_product_pricelist_purchase', False):
                        res[ai.id] = ai.partner_id.\
                            property_product_pricelist_purchase.id
                else:
                    raise osv.except_osv(_('Not Implemented!'), _(
                        """Can not compute Partner Pricelist for this"""
                        """ type of invoice: '%s'.""" % (ai.type)))
        else:
            # Normal behaviour
            # Note : In a functional field, SUPERUSER_ID is used in uid
            # So, we will used preferently context('uid') value
            if uid == SUPERUSER_ID:
                uid = context.get('uid', False) or uid

            for ai in self.browse(cr, uid, ids, context=context):
                if ai.type in ('out_invoice', 'out_refund'):
                    res[ai.id] =\
                        ai.partner_id.property_product_pricelist.id
                elif ai.type in ('in_invoice', 'in_refund'):
                    if ai.partner_id._model._columns.get(
                            'property_product_pricelist_purchase', False):
                        res[ai.id] = ai.partner_id.\
                            property_product_pricelist_purchase.id
                else:
                    raise osv.except_osv(_('Not Implemented!'), _(
                        """Can not compute Partner Pricelist for this"""
                        """ type of invoice: '%s'.""" % (ai.type)))
        return res

    # Columns Section
    _columns = {
        'partner_pricelist_id': fields.function(
            _get_partner_pricelist_id, string='Partner Pricelist',
            readonly=True, type='many2one', relation='product.pricelist',
            help="""The pricelist of the partner, when the invoice is"""
            """ created or the partner has changed. This is a technical"""
            """ field used to reporting.""",
            store={'account.invoice': (
                lambda self, cr, uid, ids, context=None: ids,
                [
                    'partner_id',
                ], 10)}),
    }
