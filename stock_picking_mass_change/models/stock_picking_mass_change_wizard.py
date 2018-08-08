# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class StockPickingMassChangeWizard(models.TransientModel):
    _name = 'stock.picking.mass.change.wizard'

    _CHANGE_METHOD_SELECTION = [
        ('fifo', 'First In First Served'),
        ('pro_rata', 'Pro Rata'),
    ]

    # Columns Section
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', required=True)

    product_uom_id = fields.Many2one(
        comodel_name='product.uom', string='UoM', required=True,
        related='product_id.uom_id', readonly=True)

    concerned_picking_qty = fields.Integer(
        string='Concerned Picking Quantity', readonly=True)

    ordered_product_qty = fields.Float(
        string='Ordered Product Quantity', readonly=True,
        digits_compute=dp.get_precision('Product Unit of Measure'))

    target_product_qty = fields.Float(
        string='Target Product Quantity', required=True, default=0,
        digits_compute=dp.get_precision('Product Unit of Measure'))

    computed_product_qty = fields.Float(
        string='Computed Product Quantity', readonly=True,
        digits_compute=dp.get_precision('Product Unit of Measure'))

    change_method = fields.Selection(
        selection=_CHANGE_METHOD_SELECTION, string='Change Method',
        required=True, default='pro_rata')

    rounding = fields.Float(
        string='Rounding', required=True, default=1,
        digits_compute=dp.get_precision('Product Unit of Measure'))

    picking_qty = fields.Integer(
        string='Selected Picking Qty', readonly=True,
        default=lambda x: x._default_picking_qty())

    line_ids = fields.One2many(
        comodel_name='stock.picking.mass.change.wizard.line',
        inverse_name='wizard_id', string='Lines')

    # Default Section
    def _default_picking_qty(self):
        return len(self._default_picking_ids())

    def _default_picking_ids(self):
        return self.env.context.get('active_ids', [])

    # On Change Section
    @api.onchange('product_id')
    def onchange_product_id(self):
        picking_obj = self.env['stock.picking']
        wizard_line_obj = self.env['stock.picking.mass.change.wizard.line']
        rounding = 1
        ordered_product_qty = 0
        concerned_picking_qty = 0
        line_vals = []
        if self.product_id:
            self.rounding = self.product_id.uom_id.rounding
            for picking in picking_obj.search(
                    [('id', 'in', self._default_picking_ids())],
                    order='date, id'):
                concerned_picking = False
                for move in picking.move_lines.filtered(
                        lambda x: x.product_id == self.product_id):
                    concerned_picking = True
                    ordered_product_qty += move.product_qty
                    line_vals.append((
                        0, 0, wizard_line_obj._prepare_from_stock_move(move)))
                if concerned_picking:
                    concerned_picking_qty += 1

        self.rounding = rounding
        self.ordered_product_qty = ordered_product_qty
        self.concerned_picking_qty = concerned_picking_qty
        self.target_product_qty = 0
        self.line_ids = line_vals

    @api.onchange('rounding', 'change_method', 'target_product_qty')
    def onchange_change_setting(self):
        total_target_qty = 0
        total_exact_target_qty = 0
        for line in self.line_ids:
            exact_target_qty = self._compute_exact_target_qty(
                line, total_exact_target_qty)
            target_qty = self._round_value(exact_target_qty)
            total_exact_target_qty += exact_target_qty
            total_target_qty += target_qty
            line.exact_target_qty = exact_target_qty
            line.target_qty = target_qty
        self.computed_product_qty = total_target_qty

    # Custom Section
    @api.multi
    def _compute_exact_target_qty(self, line, total_exact_target_qty=False):
        self.ensure_one()
        if self.change_method == 'fifo':
            qty_left = self.target_product_qty - total_exact_target_qty
            if qty_left <= 0:
                return 0
            elif qty_left < line.ordered_qty:
                return qty_left
            else:
                return line.ordered_qty
        elif self.change_method == 'pro_rata':
            return (
                line.ordered_qty / self.ordered_product_qty *
                self.target_product_qty)

    @api.multi
    def _round_value(self, value):
        self.ensure_one()
        if self.rounding:
            under = (value // self.rounding) * self.rounding
            over = ((value // self.rounding) * self.rounding) + self.rounding
            return (over - value <= value - under) and over or under
        else:
            return value

    @api.multi
    def button_apply(self):
        self.ensure_one()
        for line in self.line_ids:
            line.move_id.write({
                'name': '%s (%s -> %s)' % (
                    line.move_id.name, line.move_id.product_qty,
                    line.target_qty),
                'product_uom_qty': line.target_qty,
                'product_uom': self.product_uom_id.id,
            })
