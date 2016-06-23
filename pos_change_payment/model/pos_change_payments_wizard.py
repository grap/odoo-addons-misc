# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, _, api
from openerp.osv.osv import except_osv


class pos_change_payments_wizard(models.TransientModel):
    _name = 'pos.change.payments.wizard'

    # View Section
    def default_get(self, cr, uid, fields, context=None):
        po_obj = self.pool['pos.order']
        if context.get('active_model', False) != 'pos.order':
            raise except_osv(_('Error!'), _('Incorrect Call!'))
        res = super(pos_change_payments_wizard, self).default_get(
            cr, uid, fields, context=context)
        po = po_obj.browse(
            cr, uid, context.get('active_id'), context=context)
        res.update({'order_id': po.id})
        res.update({'session_id': po.session_id.id})
        res.update({'amount_total': po.amount_total})
        return res

    # Column Section
    order_id = fields.Many2one(
        comodel_name='pos.order', string='Order', readonly=True)
    session_id = fields.Many2one(
        comodel_name='pos.session', string='Session', readonly=True)
    line_ids = fields.One2many(
        comodel_name='pos.change.payments.wizard.line',
        inverse_name='wizard_id', string='Payment Lines')
    amount_total = fields.Float(string='Total', readonly=True)

    # Action section
    @api.multi
    def button_change_payments(self):
        wizard = self[0]
        order = wizard.order_id

        # Check if the total is correct
        total = 0
        for line in wizard.line_ids:
            total += line.amount
        if total != wizard.amount_total:
            raise except_osv(
                _('Error!'),
                _("""Differences between the two values for the POS"""
                    """ Order '%s':\n\n"""
                    """ * Total of all the new payments %s;\n"""
                    """ * Total of the POS Order %s;\n\n"""
                    """Please change the payments.""" % (
                        order.name, total, order.amount_total)))

        # Check if change payments is allowed
        order._allow_change_payments()

        # Remove old statements
        order.statement_ids.with_context(change_pos_payment=True).unlink()

        # Create new payment
        for line in wizard.line_ids:
            order.add_payment({
                'journal': int(line.bank_statement_id.journal_id.id),
                'amount': line.amount,
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
