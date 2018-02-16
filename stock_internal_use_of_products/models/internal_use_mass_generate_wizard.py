# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class InternalUseMassGenerateWizard(models.TransientModel):
    _name = 'internal.use.mass.generate.wizard'

    # Default Section
    def _default_selected_use_qty(self):
        return len(self.env.context.get('active_ids'))

    # Columns Section
    selected_use_qty = fields.Integer(
            string='Selected Internal Uses', readonly=True,
            default=_default_selected_use_qty)

    # Action Section
    @api.multi
    def apply_button(self):
        self.ensure_one()
        use_obj = self.env['internal.use']
        uses = use_obj.search([
            ('id', 'in', self.env.context.get('active_ids')),
            ('state', '=', 'confirmed')])
        return uses.action_done()
