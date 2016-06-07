# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Order Done',
    'version': '1.0',
    'category': 'Sale',
    'description': """
Improve Sale Order workflow, giving possibility to set orders to done state
===========================================================================


- sur le cancel d'un picking, lancer un run procurement des procurement lié aux
stock moves.

-> cela va mettre les sale order en exception ;

- ajouter une fonction mass editing de sale order pour traiter en masse les
sale order en exception d'envoi


Roadmap / Issue
---------------


Copyright, Author and Licence
-----------------------------

* Copyright: 2015, Groupement Régional Alimentaire de Proximité
* Author: Sylvain LE GAL (https://twitter.com/legalsylvain)
* Licence: AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'stock',
    ],
    'data': [
    ],
    'demo': [
    ],
    'installable': False,
}
