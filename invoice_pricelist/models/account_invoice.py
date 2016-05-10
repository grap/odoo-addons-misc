# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from openerp.osv import fields
from openerp.osv.orm import Model

from openerp.osv.orm import setup_modifiers
from openerp.tools.translate import _


class AccountInvoice(Model):
    _inherit = 'account.invoice'

    # Columns Section
    _columns = {
        'pricelist_id': fields.many2one(
            'product.pricelist', 'Pricelist',
            readonly=True, states={'draft': [('readonly', False)]}),
    }

    # Custom Section
    def _compute_pricelist_id(self, cr, uid, type, partner_id):
        partner_obj = self.pool['res.partner']
        if not partner_id:
            return False
        partner = partner_obj.browse(cr, uid, partner_id)
        if type in ('out_invoice', 'out_refund'):
            # Customer part
             return partner.property_product_pricelist and\
                partner.property_product_pricelist.id or False

        elif type in ('in_invoice', 'in_refund'):
            # Supplier Part
            return partner.property_product_pricelist_purchase and\
                partner.property_product_pricelist_purchase.id or False

        return False

    def create(self, cr, uid, vals, context=None):
        # Overload to avoid bugs if creation is not made by UI
        if not vals.get('pricelist_id', False):
            vals['pricelist_id'] = self._compute_pricelist_id(
                cr, uid, context.get('type', 'out_invoice'),
                vals['partner_id'])
        return super(AccountInvoice, self).create(
            cr, uid, vals, context=context)

    # View Section
    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False, submenu=False):
        context = context and context or {}
        res = super(AccountInvoice, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=False)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            nodes = doc.xpath("//field[@name='pricelist_id']")
            if nodes:
                nodes[0].set('required', '1')
                setup_modifiers(nodes[0], res['fields']['pricelist_id'])
                res['arch'] = etree.tostring(doc)
        return res

    def onchange_partner_id(
            self, cr, uid, ids, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):

        res = super(AccountInvoice, self).onchange_partner_id(
            cr, uid, ids, type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)
        res['value']['pricelist_id'] = self._compute_pricelist_id(
            cr, uid, type, partner_id)
        return res

    def onchange_pricelist_id(
            self, cr, uid, ids, pricelist_id, invoice_lines, context=None):
        pricelist_obj = self.pool['product.pricelist']
        context = context and context or {}
        if not pricelist_id:
            return {}
        value = {
            'currency_id': pricelist_obj.browse(
                cr, uid, pricelist_id, context=context).currency_id.id
        }
        if not invoice_lines:
            return {'value': value}
        warning = {
            'title': _('Pricelist Warning!'),
            'message' : _("If you change the pricelist of this invoice"
                " (and eventually the currency), prices of existing"
                " invoice lines will not be updated.")
        }
        return {'warning': warning, 'value': value}
