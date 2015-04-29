# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Food Module for Odoo
#    Copyright (C) 2012-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

import base64
import cairosvg
import StringIO

from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.translate import _

from openerp.addons.sale_food import radar_template


class product_product(Model):
    _inherit = 'product.product'

#    def _needaction_domain_get(self, cr, uid, context=None):
#        return [('pricetag_state', 'in', ('1', '2'))]

    # Constant Section
    _FRESH_CATEGORY_KEYS = [
        ('extra', 'Extra'),
        ('1', 'Category I'),
        ('2', 'Category II'),
        ('3', 'Category III'),
    ]

    _FRESH_RANGE_KEYS = [
        ('1', '1 - Fresh'),
        ('2', '2 - Canned'),
        ('3', '3 - Frozen'),
        ('4', '4 - Uncooked and Ready to Use'),
        ('4', '5 - Cooked and Ready to Use'),
    ]

    """Fields list wich modification change edition_state to 'recommanded'."""
    _PRICETAG_RECOMMANDED_FIELDS = [
        'name',
        'reference',
        'default_code',
        'social_notation',
        'local_notation',
        'organic_notation',
        'packaging_notation',
        'origin_description',
        'maker_description',
        'label_ids',
    ]
    """Fields list wich modification change edition_state to 'mandatory'."""
    _PRICETAG_MANDATORY_FIELDS = [
        'list_price',
        'volume',
        'weight_net',
        'uom_id',
    ]

    # Columns section
    def _get_price_volume(
            self, cr, uid, ids, name, arg, context=None):
        """Return the price by the volume"""
        res = {}
        for p in self.browse(cr, uid, ids, context=context):
            if p.list_price and p.volume:
                res[p.id] = "%.2f" % round(p.list_price / p.volume, 2)
            else:
                res[p.id] = ""
        return res

    def _get_price_weight_net(
            self, cr, uid, ids, name, arg, context=None):
        """Return the price by the weight_net"""
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            if product.list_price and product.weight_net:
                res[product.id] = "%.2f" % round(
                    product.list_price / product.weight_net, 2)
            else:
                res[product.id] = ""
        return res

    def _get_spider_chart_image(
            self, cr, uid, ids, field_name, arg, context=None):
        # FIXME: Translation doesn't work when installing module
        # So FR text hard-coded;
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            codeSVG = radar_template.CodeSVG % {
                'y_social': 105 - (15 * int(pp.social_notation)),
                'x_organic': 105 + (15 * int(pp.organic_notation)),
                'y_packaging': 105 + (15 * int(pp.packaging_notation)),
                'x_local': 105 - (15 * int(pp.local_notation)),
                'organic_name': _('AE'),
                'local_name': _('local'),
                'packaging_name': _('emballage'),
                'social_name': _('social'),
            }
            output = StringIO.StringIO()
            cairosvg.svg2png(bytestring=codeSVG, write_to=output)
            res[pp.id] = base64.b64encode(output.getvalue())
        return res

    def _get_pricetag_image(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            if (pp.social_notation + pp.organic_notation +
                    pp.packaging_notation + pp.local_notation) != 0:
                res[pp.id] = pp.spider_chart_image
            else:
                res[pp.id] = pp.company_id.pricetag_image
        return res

    def _get_pricetag_origin(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            tmp = ''
            if pp.origin_description:
                tmp = pp.origin_description
            if pp.department_id:
                tmp = pp.department_id.name + \
                    (' - ' + tmp if tmp else '')
            if pp.country_id:
                tmp = pp.country_id.name + \
                    (' - ' + tmp if tmp else '')
            res[pp.id] = tmp
        return res

    def _get_pricetag_color(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            if pp.pricetag_type_id:
                res[pp.id] = pp.pricetag_type_id.color
            else:
                res[pp.id] = pp.company_id.pricetag_color
        return res

    def _get_pricetag_organic_text(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pp in self.browse(cr, uid, ids, context):
            organic = False
            for pl in pp.label_ids:
                if pl.is_organic:
                    organic = True
            if organic or pp.pricetag_organic_text_ignore:
                res[pp.id] = ""
            else:
                res[pp.id] = _("Not From Organic Farming")
        return res

    def _get_extra_food_info(self, cr, uid, ids, name, arg, context=None):
        """Return extra information about food for legal documents"""
        res = {}
        if context is None:
            context = {}
        for pp in self.browse(cr, uid, ids, context=context):
            if pp.country_id:
                res[pp.id] += _(' - Country: ')\
                    + pp.country_id.name
            if pp.fresh_category:
                res[pp.id] += _(" - Category: ") + pp.fresh_category
            label = False
            for label in pp.label_ids:
                if label.mandatory_on_invoice:
                    if label:
                        label = True
                        res[pp.id] += _(" - Label: ")
                    res[pp.id] += label.name
        return res

    _columns = {
        'price_volume': fields.function(
            _get_price_volume, type='char',
            string='Price by volume'),
        'price_weight_net': fields.function(
            _get_price_weight_net, type='char',
            string='Price by weight net'),
        'country_id': fields.many2one(
            'res.country', 'Origin Country',
            help="Country of production of the product"),
        'department_id': fields.many2one(
            'res.country.department', 'Origin Department',
            help="Department of production of the product"),
        'origin_description': fields.char(
            'Origin Complement', size=64,
            help="Production location complementary information",),
        'maker_description': fields.char(
            'Maker', size=64, required=False),
        'pricetag_origin': fields.function(
            _get_pricetag_origin, type='char',
            string='Text about origin'),
        'fresh_category': fields.selection(
            _FRESH_CATEGORY_KEYS, 'Category for Fresh Product',
            help="""Extra - Hight Quality : product without default ;\n"""
            """Quality I - Good Quality : Product with little defaults ;\n"""
            """Quality II - Normal Quality : Product with default ;\n"""
            """Quality III - Bad Quality : Use this option only in"""
            """ specific situation."""),
        'fresh_range': fields.selection(
            _FRESH_RANGE_KEYS, 'Range for Fresh Product'),
        'label_ids': fields.many2many(
            'product.label', 'product_label_product_rel',
            'product_id', 'label_id', 'Labels'),
        'pricetag_type_id': fields.many2one(
            'product.pricetag.type', 'Price Tag Type'),
        'pricetag_color': fields.function(
            _get_pricetag_color, type='char',
            string="Color of the background of the Price Tag"),
        'pricetag_organic_text': fields.function(
            _get_pricetag_organic_text, type='char',
            string="Extra Text about organic origin, present on Price Tag"),
        'pricetag_organic_text_ignore': fields.boolean(
            'Ignore Organic Text on Price Tag',
            help="""If checked, the organic warning text will not be"""
            """ displayed on Price Tag, even if no organic labels are"""
            """ selected."""),
        'pricetag_state': fields.selection([
            ('0', 'Up to date'), ('1', 'Recommended'), ('2', 'Compulsory'),
            ('3', 'Do not print')], 'Price Tag State', required=True),
        'social_notation': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Social notation', required=True),
        'local_notation': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Local notation', required=True),
        'organic_notation': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Organic notation', required=True),
        'packaging_notation': fields.selection([
            ('0', 'Unknown'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
            ('5', '5')], 'Packaging notation', required=True),
        'spider_chart_image': fields.function(
            _get_spider_chart_image, type='binary', string='Spider Chart',
            store={
                'product.product': (
                    lambda self, cr, uid, ids, context=None: ids,
                    [
                        'social_notation',
                        'local_notation',
                        'organic_notation',
                        'packaging_notation',
                    ], 10)}
        ),
        'pricetag_image': fields.function(
            _get_pricetag_image, type='binary',
            string='Image on the label printed'),
        'extra_food_info': fields.function(
            _get_extra_food_info, type='char',
            string='Extra information for invoices'),
    }

    # Default Section
    _defaults = {
        'social_notation': '0',
        'local_notation': '0',
        'organic_notation': '0',
        'packaging_notation': '0',
        'pricetag_state': '2',
    }

    # Constraints section
    def _check_origin_department_country(
            self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=None):
            if pp.department_id.country_id and \
                    pp.department_id.country_id.id != \
                    pp.country_id.id:
                return False
        return True

    _constraints = [
        (
            _check_origin_department_country,
            _('Error ! Department must belong to the country.'),
            ['department_id', 'country_id']),
    ]

    # Overloads section
    def write(self, cr, uid, ids, values, context=None):
        minimum_value = 0
        if len(set(values.keys()).intersection(
                set(product_product._PRICETAG_RECOMMANDED_FIELDS))):
            minimum_value = 1
        if len(set(values.keys()).intersection(
                set(product_product._PRICETAG_MANDATORY_FIELDS))):
            minimum_value = 2
        if 'pricetag_state' in values.keys() or minimum_value == 0:
            super(product_product, self).write(
                cr, uid, ids, values, context=context)
        else:
            for product in self.browse(cr, uid, ids, context=context):
                if product.pricetag_state != 3:
                    values['pricetag_state'] = str(max(
                        minimum_value,
                        int(product.pricetag_state),
                    ))
                super(product_product, self).write(
                    cr, uid, [product.id], values, context=context)
        return True

    # Views section
    def onchange_label_ids(
            self, cr, uid, ids, label_ids, social_notation, local_notation,
            organic_notation, packaging_notation, context=None):
        ppl_obj = self.pool['product.label']
        for label in ppl_obj.browse(cr, uid, label_ids[0][2], context=context):
            social_notation = max(
                int(social_notation), int(label.minimum_social_notation))
            local_notation = max(
                int(local_notation), int(label.minimum_local_notation))
            organic_notation = max(
                int(organic_notation), int(label.minimum_organic_notation))
            packaging_notation = max(
                int(packaging_notation), int(label.minimum_packaging_notation))
        return {'value': {
            'social_notation': str(social_notation),
            'local_notation': str(local_notation),
            'organic_notation': str(organic_notation),
            'packaging_notation': str(packaging_notation),
        }}

    def onchange_department_id(
            self, cr, uid, ids, country_id, department_id, context=None):
        res = {}
        rcd_obj = self.pool['res.country.department']
        if department_id:
            rcd = rcd_obj.browse(cr, uid, department_id, context=context)
            res = {'value': {'country_id': rcd.country_id.id}}
        return res

    def onchange_country_id(
            self, cr, uid, ids, country_id, department_id, context=None):
        res = {}
        rcd_obj = self.pool['res.country.department']
        if not country_id:
            res = {'value': {'department_id': None}}
        elif department_id:
            rcd = rcd_obj.browse(cr, uid, department_id, context=context)
            if country_id != rcd.country_id.id:
                res = {'value': {'department_id': None}}
        return res
