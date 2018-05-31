# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleRecoveryPlace(models.Model):
    _name = 'sale.recovery.place'
    _order = 'name'

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    # Columns Section
    name = fields.Char('Name', required=True)

    complete_name = fields.Char(
        compute='_compute_complete_name', string='Complete Name',
        select=True, store=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', required=True,
        default=_default_company_id)

    active = fields.Boolean(string='Active', default=True)

    street = fields.Char(string='Street')

    street2 = fields.Char(string='Street2')

    zip = fields.Char(string='ZIP', change_default=True, size=24)

    city = fields.Char('City')

    state_id = fields.Many2one(
        comodel_name='res.country.state', string='State')

    country_id = fields.Many2one(comodel_name='res.country', string='Country')

    # Compute Section
    @api.multi
    @api.depends(
        'name', 'street', 'street2', 'zip', 'city', 'state_id', 'country_id')
    def _compute_complete_name(self):
        for place in self:
            address_format = place.country_id \
                and place.country_id.address_format \
                or "%(street)s\n%(street2)s\n%(city)s %(state_code)s" \
                " %(zip)s\n%(country_name)s"
            args = {
                'street': place.street or '',
                'street2': place.street2 or '',
                'zip': place.zip or '',
                'city': place.city or '',
                'state_code': place.state_id and place.state_id.code or '',
                'state_name': place.state_id and place.state_id.name or '',
                'country_code':
                    place.country_id and place.country_id.code or '',
                'country_name':
                    place.country_id and place.country_id.name or '',
            }
            place.complete_name = '%s - %s' % (
                place.name, (address_format % args).replace('\n', ' '))

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.id

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id and self.state_id:
            if self.state_id.country_id != self.country_id:
                self.state_id = False
