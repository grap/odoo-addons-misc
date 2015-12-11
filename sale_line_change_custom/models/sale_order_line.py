# -*- encoding: utf-8 -*-
##############################################################################
#    See __openerp__.py file for copyright and licences
##############################################################################

from openerp.osv.orm import Model


class sale_order_line(Model):
    _inherit = 'sale.order.line'


    def product_id_change(
            self, cr, uid, ids, pricelist, product, qty=0, uom=False,
            qty_uos=0, uos=False, name='', partner_id=False, lang=False,
            update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None):
        res = super(sale_order_line, self).product_id_change(
            cr, uid, ids, pricelist, product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order,
            packaging=packaging, fiscal_position=fiscal_position, flag=flag,
            context=context)
        if self.pool['res.users'].has_group(
                cr, uid,
                'sale_line_change_custom.group_sale_order_line_no_warning'):
            res.pop('warning', False)
        return res
