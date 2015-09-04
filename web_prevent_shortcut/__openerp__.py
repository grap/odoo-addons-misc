# -*- encoding: utf-8 -*-
##############################################################################
#
#    Web - Prevent Shortcut module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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
    'name': 'Web - Prevent Shortcut',
    'summary': 'Prevent Some Web Shortcut',
    'version': '1.0',
    'category': 'Web',
    'description': """
Web - Prevent Shortcut
======================
* if back button is pressed out of input field, the event is blocked.
  (this prevent non wanted history.back behaviour in some browsers);
* Prevent F5 reloading, if Ctrl button is not pressed;


Roadmap / Limits
----------------
* Port this module in V8;
* Make this module generic, making a web_prevent_shortcut table;
    * prevent_field : example 'BODY';
    * prevent_alt : True / False ;
    * prevent_ctrl : True / False ;
    * prevent_key_value : 116 ;
    * prevent_on_input_fields : True / False ;

    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop/',
    'depends': [
        'web',
    ],
    'js': [
        'static/src/js/web_prevent_shortcut.js'
    ],
}
