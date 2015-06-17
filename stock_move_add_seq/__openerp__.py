# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Move - Add Sequence module for Odoo
#    Copyright (C) 2013-Today Avanzosc (http://www.Avanzosc.com)
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)

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
    'name': 'Stock Move - Add Sequence',
    'version': '1.1',
    'category': 'Stock',
    'license': 'AGPL-3',
    'summary': 'Add Sequence Field on Stock Move',
    'description': """
Add Sequence Field on Stock Move
================================

* sequence field is added to stock_move;
* order of stock move is now by 'sequence' / 'date_expected' desc / 'id'
  (before, was 'date_expected' desc / 'id')
* sequence is shown in stock.picking and stock.move views;

Credits
=======

Contributors
------------
* Iker CORANTI <ikercoranti@avanzosc.com>
* Sylvain LE GAL (https://twitter.com/legalsylvain)
    """,
    'data': [
        'view/view.xml',
    ],
    'depends': [
        'stock',
    ],
    'author': 'Avanzosc,GRAP',
}
