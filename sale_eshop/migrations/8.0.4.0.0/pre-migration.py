# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

__name__ = u"[sale_eshop] refactor database"


# def add_image_write_date(cr, table_name):
#     sql = """
#         ALTER TABLE %s
#         ADD column image_write_date timestamp without time zone;
#         """ % (table_name)
#     cr.execute(sql)
#     sql = """
#         update %s set image_write_date = write_date;
#     """ % (table_name)
#     cr.execute(sql)


def set_default_value_uom_description(cr):
    sql = """
    UPDATE product_uom
    SET eshop_description = name
    WHERE eshop_description is null;
    """
    cr.execute(sql)


def migrate(cr, version):
    if not version:
        return
    set_default_value_uom_description(cr)
    # for table_name in [
    #         'product_product', 'res_company', 'eshop_category',
    #         'product_label']:
    #     add_image_write_date(cr, table_name)
