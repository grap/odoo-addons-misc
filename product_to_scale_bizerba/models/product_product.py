# -*- coding: utf-8 -*-
# Copyright (C) 2014 GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp.osv import fields
from openerp.osv.orm import Model
import openerp.addons.decimal_precision as dp


class product_product(Model):
    _inherit = 'product.product'

    # Compute Section
    def _compute_external_id_bizerba(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            res[product.id] = product.id
            if not product.scale_group_id:
                product_id_field =\
                    product.scale_group_id.scale_system_id.product_id_field_id
                if product_id_field:
                    res[product.id] = getattr(product, product_id_field.name)
        return res

    # Column Section
    _columns = {
        'scale_group_id': fields.many2one(
            'product.scale.group', string='Scale Group'),
        'external_id_bizerba': fields.function(
            _compute_external_id_bizerba, type='char',
            string='External Id for Bizerba System',
            help="External ID for bizerba system. equal to the id of the"
            " product in Odoo, of another field, depending on a setting of"
            " the the scale system of the product.\n"
            "field : product_id_field_id"),
        'scale_tare_weight': fields.float(
            digits_compute=dp.get_precision('Stock Weight'),
            string='Scale Tare Weight', help="Set here Constant tare weight"
            " for the given product. This tare will be substracted when"
            " the product is weighted. Usefull only for weightable product.\n"
            "The tare is defined with kg uom."),
    }

    # View Section
    def send_scale_create(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            self._send_to_scale_bizerba(
                cr, uid, 'create', product, context=context)
        return True

    def send_scale_write(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            self._send_to_scale_bizerba(
                cr, uid, 'write', product, context=context)
        return True

    def send_scale_unlink(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            self._send_to_scale_bizerba(
                cr, uid, 'unlink', product, context=context)
        return True

    # Custom Section
    def _send_to_scale_bizerba(self, cr, uid, action, product, context=None):
        # TODO Check if product id for bizerba is correct
        log_obj = self.pool['product.scale.log']
        scale_group_obj = self.pool['product.scale.group']
        log_obj.create(cr, uid, {
            'log_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scale_group_id': product.scale_group_id.id,
            'scale_system_id': product.scale_group_id.scale_system_id.id,
            'product_id': product.id,
            'action': action,
        }, context=context)
        # Set group as 'to refresh'
        if product.scale_group_id.screen_display and\
                not product.scale_group_id.screen_obsolete:
            scale_group_obj.write(
                cr, uid, [product.scale_group_id.id],
                {'screen_obsolete': True}, context=context)

    def _check_vals_scale_bizerba(self, cr, uid, vals, product, context=None):
        system = product.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        vals_fields = vals.keys()
        return set(system_fields).intersection(vals_fields)

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        send_to_scale = vals.get('scale_group_id', False)
        res = super(product_product, self).create(
            cr, uid, vals, context=context)
        if send_to_scale:
            product = self.browse(cr, uid, res, context=context)
            self._send_to_scale_bizerba(
                cr, uid, 'create', product, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        defered = {}
        for product in self.browse(cr, uid, ids, context=context):
            ignore = not product.scale_group_id\
                and 'scale_group_id' not in vals.keys()
            if not ignore:
                if not product.scale_group_id:
                    # (the product is new on this group)
                    defered[product.id] = 'create'
                else:
                    if vals.get('scale_group_id', False) and (
                            vals.get('scale_group_id', False) !=
                            product.scale_group_id):
                        # (the product has moved from a group to another)
                        # Remove from obsolete group
                        self._send_to_scale_bizerba(
                            cr, uid, 'unlink', product, context=context)
                        # Create in the new group
                        defered[product.id] = 'create'
                    elif self._check_vals_scale_bizerba(
                            cr, uid, vals, product, context=context):
                        # Data related to the scale
                        defered[product.id] = 'write'

        res = super(product_product, self).write(
            cr, uid, ids, vals, context=context)

        # send_image = any(['image' in x for x in bob.keys()])
        for product_id, action in defered.iteritems():
            product = self.browse(cr, uid, product_id, context=context)
            self._send_to_scale_bizerba(
                cr, uid, action, product, context=context)

        return res

    def unlink(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids, context=context):
            if product.scale_group_id:
                self._send_to_scale_bizerba(
                    cr, uid, 'unlink', product, context=context)
        return super(product_product, self).unlink(
            cr, uid, ids, context=context)
