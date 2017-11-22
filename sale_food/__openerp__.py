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
{
    'name': 'Sale - Food Information for Products',
    'version': '2.0',
    'category': 'Sales',
    'description': """
Allow users to put ethical notations on products and print pricetags
====================================================================

Functionnalities :
------------------
    * Add concept of label (organic, ...) and possibility to associate product
    to labels ;
    * Add notation on products and various information about origin, makers,
    etc...
    * Possibility to print price tags, with suggestion about wich products
    to print. (when price change for exemple) according to legal obligation.

Python librairies required on Debian System:
--------------------------------------------
    * sudo apt-get install xvfb
    * sudo nano /usr/bin/wkhtmltopdf.sh
        * #!/usr/bin/env sh
        * xvfb-run -a -s "-screen 0 640x480x16" wkhtmltopdf $*
    * sudo chmod 755 wkhtmltopdf.sh


TODO
----

new model:
* res.company.certification
    * company_id
    * organization_id
    * date_start (default = get last end date);
    * date_end (default = 31/12/Current_year);

* res.partner.certification
    * partner_id
    * organization_id
    * date_start (default = get last end date);
    * date_end (default = 31/12/Current_year);

    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'l10n_fr_department',
        'report_webkit',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir_module_category.yml',
        'security/res_groups.yml',
        'security/ir_model_access.yml',
        'report/pricetag_report.xml',
        'report/pricetag_report_tall.xml',
        'report/pricetag_report_small.xml',
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
        'data/ir_header_webkit.xml',
        'data/ir_property.xml',
    ],
    'demo': [
        'demo/product_label.yml',
        'demo/product_pricetag_type.yml',
        'demo/function.xml',
        'demo/res_groups.yml',
    ],
    'css': [
        'static/src/css/css.css',
    ],
    'external_dependencies': {
        'python': ['cairosvg'],
        'bin': ['wkhtmltopdf'],
    },
}
