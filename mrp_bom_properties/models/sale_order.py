# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    property_ids = fields.Many2many(
        'mrp.bom.property',
        'sale_mrp_bom_property_rel',
        'order_id',
        'property_id',
        'Properties',
        readonly=True,
        states={'draft': [('readonly', False)]})
