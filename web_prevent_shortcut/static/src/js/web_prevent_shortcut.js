/******************************************************************************
    Web - Prevent Shortcut module for Odoo
    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
******************************************************************************/

$(function(){
    /*
     * this swallows some keys depending of settings.
     */
    var NON_INPUT_FIELDS = ['A', 'BODY']

    $(document).bind("keydown keypress", function(e){

        // we prevent F5 pressed, if not Ctr is pressed
        if (e.which == 116){
            if (! e.ctrlKey){
                e.preventDefault();
            }
        } 
         // Prevent backspace on non input field
        if(e.which == 8){
            if ($.inArray(e.target.tagName, NON_INPUT_FIELDS) != -1){
                e.preventDefault();
            }
        }
    });
});
