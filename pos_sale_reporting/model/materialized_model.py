# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale / Sale Reporting module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

import logging

from openerp import SUPERUSER_ID
from openerp.osv.orm import Model

_logger = logging.getLogger(__name__)


class MaterializedModel(Model):
    """Main super-class for Model based on MATERIALIZED VIEW.

    Odoo models are created by inheriting from this class::

        class user(MaterializedModel):
            ...
    """
    _auto = True
    _register = False
    _transient = False

    _materialized_sql = ''

    _materialized_module_name = ''

    _is_materialized = False

    def __init__(self, pool, cr):
        super(MaterializedModel, self).__init__(pool, cr)
        cr.execute("SELECT version();")
        res = cr.fetchall()
        self._is_materialized = res[0][0].split(" ")[1] >= '9.3'

    def init(self, cr):
        if self._is_materialized:
            # Creating materialized view only if module state is 'to install'
            imm_obj = self.pool['ir.module.module']
            imm_id = imm_obj.search(cr, SUPERUSER_ID, [
                ('name', '=', 'pos_sale_reporting'),
                ('state', '=', 'to install')])
            if len(imm_id) != 0:
                self._create_view(cr, SUPERUSER_ID)
        else:
            self._create_view(cr, SUPERUSER_ID)

    def _create_view(self, cr, uid, context=None):
        if self._is_materialized:
            _logger.info("Creating MATERIALIZED VIEW %s" % (
                self._table_name))
            cr.execute("""
                DROP MATERIALIZED VIEW IF EXISTS %s;
                CREATE MATERIALIZED VIEW %s AS (%s);""" % (
                self._table_name, self._table_name,
                self._materialized_sql))
        else:
            cr.execute("""
                DROP VIEW IF EXISTS %s;
                CREATE VIEW %s AS (%s);""" % (
                self._table_name, self._table_name,
                self._materialized_sql))

    def _refesh_view(self, cr, uid, context=None):
        if self._is_materialized:
            _logger.info("Refreshing MATERIALIZED VIEW %s" % (
                self._table_name))
            cr.execute("REFRESH MATERIALIZED VIEW %s;" % (self._table_name))
        else:
            _logger.warning(
                "Unable to refresh %s because it is not an"
                " materialized view" % (self._table_name))
