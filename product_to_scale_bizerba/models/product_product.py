# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

import openerp.addons.decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Column Section
    scale_group_id = fields.Many2one(
        comodel_name='product.scale.group', string='Scale Group')

    external_id_bizerba = fields.Char(
        compute='_compute_external_id_bizerba',
        string='External Id for Bizerba System',
        help="External ID for bizerba system. equal to the id of the"
        " product in Odoo, of another field, depending on a setting of"
        " the the scale system of the product.\n"
        "field : product_id_field_id")

    scale_tare_weight = fields.Float(
        digits_compute=dp.get_precision('Stock Weight'),
        string='Scale Tare Weight', help="Set here Constant tare weight"
        " for the given product. This tare will be substracted when"
        " the product is weighted. Usefull only for weightable product.\n"
        "The tare is defined with kg uom.")

    # Compute Section
    @api.multi
    def _compute_external_id_bizerba(self):
        for product in self:
            if product.scale_group_id:
                product_id_field =\
                    product.scale_group_id.scale_system_id.product_id_field_id
                if product_id_field:
                    product.external_id_bizerba =\
                        getattr(product, product_id_field.name)

    # View Section
    @api.multi
    def send_scale_create(self):
        for product in self:
            product._send_to_scale_bizerba(
                'create', product.scale_group_id,
                product.scale_group_id.scale_system_id)

    @api.multi
    def send_scale_write(self):
        for product in self:
            product._send_to_scale_bizerba(
                'write', product.scale_group_id,
                product.scale_group_id.scale_system_id)

    @api.multi
    def send_scale_unlink(self):
        for product in self:
            product._send_to_scale_bizerba(
                'unlink', product.scale_group_id,
                product.scale_group_id.scale_system_id)

    # Custom Section
    @api.multi
    def _send_to_scale_bizerba(self, action, scale_group, scale_system):
        self.ensure_one()
        product = self

        log_obj = self.env['product.scale.log']

        if not product.external_id_bizerba:
            raise UserError(_(
                "You have to set the field '%s' used as an ID for the Bizerba"
                " if you set scale category to this product %s" % (
                    scale_system.product_id_field_id.name,
                    product.name)))

        log_obj.create({
            'log_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scale_group_id': scale_group.id,
            'scale_system_id': scale_system.id,
            'product_id': product.id,
            'action': action
        })
        # Set group as 'to refresh'
        if product.scale_group_id.screen_display and\
                not product.scale_group_id.screen_obsolete:
            product.scale_group_id.write({
                'screen_obsolete': True,
            })

    @api.multi
    def _check_vals_scale_bizerba(self, vals):
        self.ensure_one()
        system = self.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        vals_fields = vals.keys()
        return set(system_fields).intersection(vals_fields)

    # Overload Section
    @api.multi
    def copy(self, default=None):
        default = default and default or {}
        default['scale_group_id'] = False
        return super(ProductProduct, self).copy(default=default)

    @api.model
    def create(self, vals):
        send_to_scale = vals.get('scale_group_id', False)
        product = super(ProductProduct, self).create(vals)
        if send_to_scale:
            product._send_to_scale_bizerba(
                'create', product.scale_group_id,
                product.scale_group_id.scale_system_id)
        return product

    @api.multi
    def write(self, vals):
        defered = {}
        for product in self:
            if product.scale_group_id:
                # The product is currently in a group (before update)
                if 'scale_group_id' not in vals.keys():
                    # Regular update of some informations
                    if product._check_vals_scale_bizerba(vals):
                        # Data related to the scale
                        defered[product.id] = 'write'
                else:
                    if vals.get('scale_group_id') is False:
                        # the product has moved out of the scale group
                        # Remove from obsolete group
                        product._send_to_scale_bizerba(
                            'unlink', product.scale_group_id,
                            product.scale_group_id.scale_system_id)
                    else:
                        # The product move from a category to another
                        # Remove from obsolete group
                        product._send_to_scale_bizerba(
                            'unlink', product.scale_group_id,
                            product.scale_group_id.scale_system_id)
                        # Create in the new group
                        defered[product.id] = 'create'
            else:
                # The product is not currently in a group
                if 'scale_group_id' in vals.keys():
                    # The product has just been added
                    defered[product.id] = 'create'

        res = super(ProductProduct, self).write(vals)

        # Send Deferred Log
        for product_id, action in defered.iteritems():
            product = self.browse(product_id)
            product._send_to_scale_bizerba(
                action, product.scale_group_id,
                product.scale_group_id.scale_system_id)

        return res

    @api.multi
    def unlink(self):
        for product in self:
            if product.scale_group_id:
                product._send_to_scale_bizerba(
                    'unlink', product.scale_group_id,
                    product.scale_group_id.scale_system_id)
        return super(ProductProduct, self).unlink()
