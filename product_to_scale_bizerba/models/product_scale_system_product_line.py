# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductScaleSystemProductLine(models.Model):
    _name = 'product.scale.system.product.line'
    _order = 'scale_system_id, sequence'

    _TYPE_SELECTION = [
        ('id', 'Product ID'),
        ('numeric', 'Numeric Field'),
        ('text', 'Char / Text Field'),
        ('external_text', 'External Text Field'),
        ('constant', 'Constant Value'),
        ('external_constant', 'External Constant Text Value'),
        ('many2one', 'ManyOne Field'),
        ('many2many', 'Many2Many Field'),
        ('product_image', 'Product Image'),
    ]

    # Column Section
    scale_system_id = fields.Many2one(
        comodel_name='product.scale.system', string='Scale System',
        required=True, ondelete='cascade', select=True)

    company_id = fields.Many2one(
        related='scale_system_id.company_id', string='Company',
        comodel_name='res.company', store=True, select=True)

    code = fields.Char(string='Bizerba Code', required=True)

    name = fields.Char(string='Name', required=True)

    sequence = fields.Integer(string='Sequence', default=10)

    type = fields.Selection(selection=_TYPE_SELECTION, string='Type')

    field_id = fields.Many2one(
        comodel_name='ir.model.fields', string='Product Field',
        domain=[('model', 'in', ['product.product', 'product.template'])])

    # TODO Improve. Set domain, depending on the other field
    related_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='M2M / M2O Field', help="Used only"
        " for the x2x fields. Set here the field of the related model"
        " that you want to send to the scale. Let empty to send the ID.")

    x2many_range = fields.Integer(
        string='range of the x2Many Fields', help="Used if type is"
        " 'Many2Many Field', to mention the"
        " range of the field  to send. Begin by 0. (used for exemple"
        " for product logos)")

    constant_value = fields.Char(
        string='Constant Value', help="Used if type is 'constant',"
        " to send allways the same value.")

    multiline_length = fields.Integer(
        string='Length for Multiline', default=0,
        help="Used if type is 'Text Field' or 'External Text Constant', to"
        " indicate the max length of a line. Set 0 to avoid to split the"
        " value.")

    multiline_separator = fields.Char(
        string='Separator for Multiline', default='\n', help="Used if type is"
        " 'Text Field' or 'External Text Constant', to indicate wich text"
        " will be used to mention break lines.")

    # TODO Improve. Set contrains.
    numeric_coefficient = fields.Float(
        string='Numeric Coefficient', default=1, help="Used if type is"
        " 'Numeric Field', to mention with coefficient numeric"
        " field should be multiplyed.")

    numeric_round = fields.Float(
        string='Rounding Method', default=1, help="Used if type is"
        " 'Numeric Field', to mention how the value should be rounded.\n"
        " Do not Use 0, because it will truncate the value.")

    delimiter = fields.Char(
        string='Delimiter Char', default='#', help="Used to finish the column")
