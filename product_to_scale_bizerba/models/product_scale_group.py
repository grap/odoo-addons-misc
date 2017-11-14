# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class product_scale_group(Model):
    _name = 'product.scale.group'

    # Compute Section
    def _compute_product_qty(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for group in self.browse(cr, uid, ids, context):
            res[group.id] = len(group.product_ids)
        return res

    def _compute_last_product_position(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for group in self.browse(cr, uid, ids, context):
            res[group.id] = group.screen_offset + group.screen_product_qty - 1
        return res

    # Column Section
    _columns = {
        'name': fields.char(
            string='Name', required=True),
        'active': fields.boolean(
            string='Active'),
        'external_shelf_id': fields.char(
            string='External Shelf ID', required=True, help="Unused field"
            " for the time being. Define shelf products."),
        'external_family_id': fields.char(
            string='External Family ID', required=True, help="this value will"
            " be used in the KEY file, send to Scales, that specify"
            " production position on Customer Scale."),
        'screen_display': fields.boolean(
            string='Display on Screen', help="Check this box if you want"
            " to display the products on Customer Scale."),
        'screen_obsolete': fields.boolean(
            string='Screen Obsolete', readonly=True,
            help="This box is checked if the display of screen is obsolete"),
        'screen_offset': fields.integer(
            string='Screen Offset'),
        'last_product_position': fields.function(
            _compute_last_product_position, type='integer',
            string='Last Product Position'),
        'screen_product_qty': fields.integer(
            string='Products quantity on Screen', help="Set the number of"
            " products available for this Scale group.\n"
            " Set 0, if your scale do not have tactile screen."),
        'company_id': fields.related(
            'scale_system_id', 'company_id', type='many2one', store=True,
            relation='res.company', string='Company', readonly='True'),
        'scale_system_id': fields.many2one(
            'product.scale.system', string='Scale System', required=True),
        'product_ids': fields.one2many(
            'product.product', 'scale_group_id', 'Products'),
        'product_qty': fields.function(
            _compute_product_qty, type='integer', string='Products Quantity'),
    }

    _defaults = {
        'active': True,
        'external_shelf_id': 1,
        'external_family_id': 1,
        'screen_obsolete': False,
    }
