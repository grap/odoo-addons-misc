# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, exceptions


class PosChangePaymentsWizard(models.TransientModel):
    _name = 'pos.change.payments.wizard'

    # View Section
    @api.model
    def default_get(self, fields):
        order_obj = self.env['pos.order']
        res = super(PosChangePaymentsWizard, self).default_get(fields)
        if self.env.context.get('active_model', False) == 'pos.order':
            order = order_obj.browse(self.env.context.get('active_id'))
            res.update({
                'order_id': order.id,
                'amount_total': order.amount_total,
            })
        return res

    # Column Section
    order_id = fields.Many2one(
        comodel_name='pos.order', string='POS Order', required=True,
        readonly=True)
    line_ids = fields.One2many(
        comodel_name='pos.change.payments.wizard.line',
        inverse_name='wizard_id', string='Wizard Lines')
    amount_total = fields.Float(
        string='Total', readonly=True)

    # View section
    @api.multi
    def button_change_payments(self):
        pass
#        order_obj = self.env['pos.order']
#        statement_line_obj = self.env['account.bank.statement.line']

#        ctx = context.copy()
#        ctx['change_pos_payment'] = True

#        for pcpw in self.browse(cr, uid, ids, context=context):
#            po = order_obj.browse(cr, uid, pcpw.order_id.id, context=context)

#            # Check if the total is correct
#            total = 0
#            for line in pcpw.line_ids:
#                total += line.amount
#            if total != pcpw.amount_total:
#                raise except_osv(
#                    _('Error!'),
#                    _("""Differences between the two values for the POS"""
#                        """ Order '%s':\n\n"""
#                        """ * Total of all the new payments %s;\n"""
#                        """ * Total of the POS Order %s;\n\n"""
#                        """Please change the payments.""" % (
#                            po.name, total, po.amount_total)))

#            # Check if change payments is allowed
#            order_obj._allow_change_payments(
#                cr, uid, [po.id], context=context)

#            # Remove old statements
#            statement_line_obj.unlink(
#                cr, uid, [x.id for x in po.statement_ids], context=ctx)

#            # Create new payment
#            for line in pcpw.line_ids:
#                order_obj.add_payment(cr, uid, po.id, {
#                    'journal': int(line.journal_id),
#                    'amount': line.amount,
#                }, context=context)

##        return {
##            'type': 'ir.actions.client',
##            'tag': 'reload',
##        }
