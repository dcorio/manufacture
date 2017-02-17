# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def _get_matching_bom(self):
        if self.bom_id:
            return self.bom_id
        return self.env['mrp.bom'].with_context(
            company_id=self.company_id.id, force_company=self.company_id.id
        )._bom_find_prop(
            product=self.product_id,
            picking_type=self.rule_id.picking_type_id,
            procurement_id=self)
