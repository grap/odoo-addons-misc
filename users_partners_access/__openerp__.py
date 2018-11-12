# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Users Partners access',
    'summary': 'Users Partners Access',
    'version': '8.0.3.0.0',
    'category': 'base',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
