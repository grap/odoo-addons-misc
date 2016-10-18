# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import netsvc
from openerp.osv import orm, fields
from openerp.osv.osv import except_osv
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp


class StockPickingQuickInvoiceWizard(orm.TransientModel):
    _name = 'stock.picking.quick.invoice.wizard'

    _columns = {
        'state': fields.selection([
            ('picking_invoice', 'Picking and Invoice'),
            ('payment', 'Payment')], 'Status', readonly=True),
        'picking_id': fields.many2one(
            'stock.picking', 'Delivery Order', readonly=True,
            required=True),
        'date_invoice': fields.date(
            'Invoice Date', readonly=True,
            help="Keep empty to use the current date", required=True),
        'invoice_id': fields.many2one(
            'account.invoice', 'Invoice', readonly=True),
        'amount_total': fields.related(
            'invoice_id', 'amount_total', readonly=True,
            digits_compute=dp.get_precision('Account'), string='Total'),
        'line_ids': fields.one2many(
            'stock.picking.quick.invoice.line.wizard',
            'wizard_id', 'Payments'),
    }

    def _default_picking_id(self, cr, uid, context=None):
        return context.get('active_id', False)

    def _default_date_invoice(self, cr, uid, context=None):
        return fields.date.context_today(self, cr, uid)

    _defaults = {
        'state': 'picking_invoice',
        'picking_id': _default_picking_id,
        'date_invoice': _default_date_invoice,
    }

    def button_quick_picking_invoice(self, cr, uid, ids, context=None):
        picking_obj = self.pool['stock.picking']
        invoice_obj = self.pool['account.invoice']
        journal_obj = self.pool['account.journal']
        picking_wizard_obj = self.pool['stock.partial.picking']
        invoice_wizard_obj = self.pool['stock.invoice.onshipping']

        wizard = self.browse(cr, uid, ids[0], context=context)
        picking = wizard.picking_id

        # Check State
        if picking.invoice_state != '2binvoiced':
            raise except_osv(_('Error!'), _(
                "Unable to invoice a picking that is not marked as "
                "'To be invoiced'."))

        # Force assign (if not done)
        if picking.state in ['draft', 'auto', 'confirmed']:
            picking_obj.action_assign(cr, uid, [picking.id], context)
            picking_obj.force_assign(cr, uid, [picking.id])

        # Deliver (if not done)
        if picking.state in ['draft', 'auto', 'confirmed', 'assigned']:
            process_wizard_id = picking_wizard_obj.create(
                cr, uid, {}, context=context)
            picking_wizard_obj.do_partial(
                cr, uid, [process_wizard_id], context=context)

        # Create invoice
        invoice_wizard_id = invoice_wizard_obj.create(
            cr, uid, {'invoice_date': wizard.date_invoice}, context=context)
        invoice_res = invoice_wizard_obj.create_invoice(
            cr, uid, [invoice_wizard_id], context=context)
        invoice_id = invoice_res[picking.id]

        # Validate invoice
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(
            uid, 'account.invoice', invoice_id, 'invoice_open', cr)
        invoice = invoice_obj.browse(cr, uid, invoice_id, context=context)

        wizard_vals = {
            'invoice_id': invoice_id,
            'state': 'payment',
        }

        journal_id = journal_obj.search(cr, uid, [
            ('type', 'in', ['bank', 'cash']),
            ('is_default_quick_payment', '=', True)], limit=1)
        if journal_id:
            wizard_vals['line_ids'] = [(0, False, {
                'journal_id': journal_id[0],
                'amount': invoice.amount_total,
            })]

        self.write(cr, uid, [wizard.id], wizard_vals, context=context)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking.quick.invoice.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wizard.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def button_quick_payment(self, cr, uid, ids, context=None):
        voucher_obj = self.pool['account.voucher']
        partner_obj = self.pool['res.partner']

        wizard = self.browse(cr, uid, ids[0], context=context)

        # Check value
        total_payment = sum([x.amount for x in wizard.line_ids])
        if wizard.amount_total != total_payment:
            raise except_osv(_('Error!'), _(
                "The sum of payment %d is not the same as the invoice total"
                " %d.") % (total_payment, wizard.amount_total))

        # Create payment
        voucher_ids = []
        partner_id = partner_obj._find_accounting_partner(
            wizard.invoice_id.partner_id).id
        for line in wizard.line_ids:
            ctx = context.copy()
            ctx['invoice_id'] = wizard.invoice_id
            voucher_vals = voucher_obj.onchange_partner_id(
                cr, uid, False, wizard.invoice_id.partner_id.id,
                line.journal_id.id, line.amount,
                wizard.invoice_id.currency_id.id,
                'sale', wizard.date_invoice, context=context)['value']
            voucher_vals.update(voucher_obj.onchange_amount(
                cr, uid, False, line_ids=False, tax_id=False,
                price=line.amount, partner_id=partner_id,
                journal_id=line.journal_id.id,
                ttype='sale', company_id=wizard.invoice_id.company_id.id,
                context=context)['value'])
            voucher_vals.update({
                'partner_id': wizard.invoice_id.partner_id.id,
                'amount': line.amount,
                'journal_id': line.journal_id.id,
                'date': wizard.date_invoice,
                'reference': wizard.invoice_id.name,
                'type': 'receipt',
            })
            voucher_id = voucher_obj.create(
                cr, uid, voucher_vals, context=context)
            voucher_ids.append(voucher_id)

        voucher_obj.button_proforma_voucher(
            cr, uid, voucher_ids, context=context)
        return True
