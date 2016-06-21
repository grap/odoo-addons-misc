/*
Copyright (C) 2015-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

openerp.pos_tare = function(instance){
    var module = instance.point_of_sale;
    _t = instance.web._t;

    /*************************************************************************
        Extend : Widget 'PosWidget'
    */
    module.PosWidget = module.PosWidget.extend({
        build_widgets: function(){
            this._super();

            // Add a new screen 'TareScreenWidget'
            this.tare_screen = new module.TareScreenWidget(this,{});
            this.tare_screen.appendTo(this.$('.screens'));
            this.screen_selector.add_screen('tare', this.tare_screen);
        },
    });

    /*************************************************************************
        Extend : Widget 'ScaleScreenWidget'
    */
    module.ScaleScreenWidget = module.ScaleScreenWidget.extend({
        next_screen: 'tare',

        // Overwrite 'show' function to display TareScreenWidget
        show: function(){
            this.pos_widget.screen_selector.set_current_screen(this.next_screen,{product: this.get_product()});
        },
    });

    /*************************************************************************
        Define : New Widget 'TareScreenWidget'
    */
    module.TareScreenWidget = module.ScreenWidget.extend({
        template:'TareScreenWidget',
        next_screen: 'products',
        previous_screen: 'products',
        show_leftpane: false,

        init: function(parent, options) {
            this._super(parent, options);
            this.gross_weight = 0;
            this.tare_weight = 0;
            this.net_weight = 0;
        },

        show: function(){
            this.current_product = this.get_product();
            this.current_product_name = this.get_product().display_name;
            this.current_unit_price = this.get_product().price;
            this._super();
            this.renderElement();
            var self = this;
            this.gross_weight = 0;
            this.tare_weight = 0;
            this.net_weight = 0;

            this.add_action_button({
                    label: _t('Back'),
                    icon: '/point_of_sale/static/src/img/icons/png48/go-previous.png',
                    click: function(){  
                        self.pos_widget.screen_selector.set_current_screen(self.previous_screen);
                    },
                });

            this.order_button = this.add_action_button({
                    label: _t('Order'),
                    icon: '/point_of_sale/static/src/img/icons/png48/go-next.png',
                    click: function() { self.order_product_click(); },
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
            this.order_button.set_disabled(true);
        },

        updateValidNetWeight: function(){
            // get a number without floating bug
            this.net_weight = (this.gross_weight - this.tare_weight).toFixed(3);
            this.$('#net-weight')[0].value = this.net_weight;
            var price = this.current_product.price * this.net_weight;
            this.$('#total-price')[0].value = price.toFixed(2);
            this.order_button.set_disabled(false);
        },

        get_product: function(){
            var ss = this.pos_widget.screen_selector;
            if(ss){
                return ss.get_current_screen_param('product');
            }else{
                return undefined;
            }
        },

        order_product_click: function(){
            this.pos.get('selectedOrder').addProduct(this.current_product,{ quantity:this.net_weight });
            this.pos_widget.screen_selector.set_current_screen(this.next_screen);
        },

    });
};





