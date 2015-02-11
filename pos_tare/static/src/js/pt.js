/******************************************************************************
    Point Of Sale - Tare module for OpenERP
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

openerp.pos_tare = function(instance){
    var module = instance.point_of_sale;

    module.PosWidget = module.PosWidget.extend({
        build_widgets: function(){
            // Add a new screen 'TareScreenWidget'
            this.tare_screen = new module.TareScreenWidget(this,{});
            this.tare_screen.appendTo($('#rightpane'));
            this._super();
            this.screen_selector.add_screen('tare', this.tare_screen);
        },
    });

    /*************************************************************************
        Overload : Widget 'ScaleScreenWidget'
    */
    module.ScaleInviteScreenWidget = module.ScaleInviteScreenWidget.extend({
        next_screen: 'tare',

        // Overwrite 'show' function to display TareScreenWidget
        show: function(){
            this.pos_widget.screen_selector.set_current_screen(this.next_screen);
        },
    });

    /*************************************************************************
        Define : New Widget 'TareScreenWidget'
    */
    module.TareScreenWidget = module.ScreenWidget.extend({
        template:'TareScreenWidget',

        next_screen: 'products',
        previous_screen: 'products',

        init: function(parent, options) {
            this._super(parent, options);
            this.gross_weight = 0;
            this.tare_weight = 0;
            this.net_weight = 0;
        },

        show: function(){
            this._super();
            this.renderElement();
            var self = this;
            this.gross_weight = 0;
            this.tare_weight = 0;
            this.net_weight = 0;

            // Add 'Cancel' Button
            this.add_action_button({
                label: _t('Back'),
                icon: '/point_of_sale/static/src/img/icons/png48/go-previous.png',
                click: function(){
                    self.pos_widget.screen_selector.set_current_screen(self.previous_screen);
                }
            });

            // Add 'Validate' Button
            this.validate_button = this.add_action_button({
                label: _t('Validate'),
                icon: '/point_of_sale/static/src/img/icons/png48/validate.png',
                click: function(){
                    self.order_product();
                    self.pos_widget.screen_selector.set_current_screen(self.next_screen);
                },
            });

            // Focus on Gross Weight
            this.$('#gross-weight').focus();

            // Disable Validate Button
            this.updateInvalidNetWeight();
        },

        renderElement: function() {
            this._super();
            var self = this;
            this.$('#gross-weight').keyup(function(event){
                self.changeGrossWeight(event);
            });
            this.$('#tare-weight').keyup(function(event){
                self.changeTareWeight(event);
            });
        },

        changeGrossWeight: function(event) {
            var newGrossWeight = event.currentTarget.value;
            grossWeight = parseFloat(newGrossWeight.replace(',', '.'));
            if(!isNaN(grossWeight) && newGrossWeight.trim() != ''){
                this.gross_weight = grossWeight;
                this.updateValidNetWeight();
            }
            else{
                this.updateInvalidNetWeight();
            }
        },

        changeTareWeight: function(event) {
            var newTareWeight = event.currentTarget.value;
            tareWeight = parseFloat(newTareWeight.replace(',', '.'));
            if(!isNaN(tareWeight) && newTareWeight.trim() != ''){
                this.tare_weight = tareWeight;
                this.updateValidNetWeight();
            }
            else{
                this.updateInvalidNetWeight();
            }
        },

        updateInvalidNetWeight: function(){
            this.validate_button.set_disabled(true);
        },

        updateValidNetWeight: function(){
            // get a number without floating bug
            this.net_weight = (this.gross_weight - this.tare_weight ).toFixed(3);
            this.$('#net-weight').html(this.net_weight);
            var price = this.get_product().get('price') * this.net_weight;
            this.$('#total-price').html(price.toFixed(2));
            
            this.validate_button.set_disabled(false);
        },

        get_product: function(){
            var ss = this.pos_widget.screen_selector;
            if(ss){
                return ss.get_current_screen_param('product');
            }else{
                return undefined;
            }
        },

        get_product_name: function(){
            var product = this.get_product();
            return (product ? product.get('name') : undefined) || 'Unnamed Product';
        },

        order_product: function(){
            this.pos.get('selectedOrder').addProduct(this.get_product(),{ quantity:this.net_weight });
        },

    });
};





