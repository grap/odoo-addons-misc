# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models, tools
from openerp.exceptions import Warning as UserError


class EshopCategory(models.Model):
    _name = 'eshop.category'
    _inherit = ['eshop.with.image.mixin']
    _rec_name = 'complete_name'
    _order = 'sequence, complete_name'

    # Inherit Section
    _eshop_invalidation_type = 'single'

    _eshop_invalidation_fields = [
        'name', 'available_product_qty', 'child_qty', 'image_medium',
        'type', 'parent_id', 'product_ids', 'complete_name',
    ]

    _eshop_image_fields = ['image', 'image_medium', 'image_small']

    _TYPE_SELECTION = [
        ('view', 'View'),
        ('normal', 'Normal'),
    ]

    # Columns Section
    name = fields.Char(string='Name', required=True, select=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', select=True,
        required=True, default=lambda s: s._default_company_id())

    sequence = fields.Integer(string='Sequence', required=True, default=1)

    complete_name = fields.Char(
        string='Name', store=True, compute='_compute_complete_name')

    image = fields.Binary(string='Image')

    image_medium = fields.Binary(
        compute='_compute_multi_image',
        string='Medium-sized image', store=True)

    image_small = fields.Binary(
        compute='_compute_multi_image',
        string='Small-sized image', store=True)

    parent_id = fields.Many2one(
        comodel_name='eshop.category', string='Parent Category',
        select=True, domain="[('type', '=', 'view')]")

    child_ids = fields.One2many(
        comodel_name='eshop.category', inverse_name='parent_id',
        string='Child Categories', readonly=True)

    type = fields.Selection(
        selection=_TYPE_SELECTION, string='Category Type', required=True,
        default='normal',
        help="A category of the view type is a virtual category that"
        " can be used as the parent of another category to create a"
        " hierarchical structure.")

    product_ids = fields.One2many(
        comodel_name='product.product', inverse_name='eshop_category_id',
        string='Products', readonly=True)

    child_qty = fields.Integer(
        string='Childs Quantity', compute='_compute_multi_child')

    product_qty = fields.Integer(
        string='Products Quantity', compute='_compute_multi_child')

    available_product_ids = fields.One2many(
        string='Available Products', compute='_compute_multi_child',
        comodel_name='product.product')

    available_product_qty = fields.Integer(
        string='Available Products Quantity', compute='_compute_multi_child',
        comodel_name='product.product')

    # Default Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    # Constraints Section
    @api.constrains('type', 'product_ids', 'child_ids')
    def _check_type(self):
        for category in self:
            if category.type == 'view' and category.product_qty > 0:
                raise UserError(_(
                    "A 'view' Category can not belongs products"))
            elif category.type == 'normal' and len(category.child_ids) > 0:
                raise UserError(_(
                    "A 'normal' Category can not belongs childs categories"))

    # Compute Section
    @api.multi
    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = _("%s / %s") % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.multi
    @api.depends('product_ids', 'child_ids')
    def _compute_multi_child(self):
        ProductProduct = self.env['product.product']
        all_product_ids = ProductProduct.search([
            ('eshop_category_id', 'in', self.ids),
        ]).ids
        all_available_product_ids = ProductProduct.search([
            ('id', 'in', all_product_ids),
            ('eshop_state', '=', 'available'),
        ]).ids
        for category in self:
            product_ids = category.product_ids.ids
            available_product_ids = list(
                set(all_available_product_ids) & set(product_ids))
            category.product_qty = len(product_ids)
            category.available_product_ids = available_product_ids
            category.available_product_qty = len(available_product_ids)
            category.child_qty = len(category.child_ids)

    @api.multi
    @api.depends('image')
    def _compute_multi_image(self):
        for category in self:
            image_data = tools.image_get_resized_images(
                category.image, avoid_resize_medium=True)
            category.image_small = image_data['image_small']
            category.image_medium = image_data['image_medium']

    # @api.multi
    # def _set_image(self, cr, uid, pId, name, value, args, context=None):
    #     return self.write(
    #         cr, uid, [pId], {'image': tools.image_resize_image_big(value)},
    #         context=context)

    # Overload Section
    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        self._write_eshop_invalidate(vals)
        return super(EshopCategory, self).write(vals)

    # Name Function
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        recs = self.search(
            [('complete_name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.multi
    @api.depends('complete_name')
    def name_get(self):
        res = []
        for category in self:
            res.append((category.id, category.complete_name))
        return res
