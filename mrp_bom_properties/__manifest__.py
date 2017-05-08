# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP BoM Properties',
    'summary': """
        MRP BoM Properties""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Davide Corio,Odoo Community Association (OCA)',
    'website': 'http://davidecorio.com',
    'depends': [
        'mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_view.xml',
        'views/sale_order_view.xml'
    ],
    'demo': [
    ],
    'installable': True,
}
