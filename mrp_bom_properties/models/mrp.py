# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MrpBomPropertyGroup(models.Model):
    _name = 'mrp.bom.property.group'
    _description = 'Property Group'

    name = fields.Char('Property Group', required=True)
    description = fields.Text('Description')


class MrpBomProperty(models.Model):
    _name = 'mrp.bom.property'
    _description = 'BoM Property'

    name = fields.Char('Name', required=True)
    group_id = fields.Many2one(
        'mrp.bom.property.group', 'BoM Property Group', required=True)
    description = fields.Text('Description')


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    property_ids = fields.Many2many('mrp.bom.property', string='Properties')

    @api.model
    def _bom_find_prop(
            self, product_tmpl=None, product=None, picking_type=None,
            company_id=False, procurement_id=None):
        if product:
            if not product_tmpl:
                product_tmpl = product.product_tmpl_id
            domain = [
                '|',
                ('product_id', '=', product.id),
                '&',
                ('product_id', '=', False),
                ('product_tmpl_id', '=', product_tmpl.id)]
        elif product_tmpl:
            domain = [('product_tmpl_id', '=', product_tmpl.id)]
        else:
            return False
        if picking_type:
            domain += [
                '|',
                ('picking_type_id', '=', picking_type.id),
                ('picking_type_id', '=', False)]
        if company_id or self.env.context.get('company_id'):
            domain = domain + [
                ('company_id', '=', company_id or self.env.context.get(
                    'company_id'))]
        res = self.search(domain, order='sequence, product_id')
        property_ids = []
        if procurement_id:
            for procurement in procurement_id.group_id.procurement_ids:
                if (procurement.sale_line_id and
                        procurement.sale_line_id.property_ids):
                    for property_id in procurement.sale_line_id.property_ids:
                        property_ids.append(property_id)
        bom_empty_prop = False
        properties = [p.id for p in property_ids]
        for bom in res:
            if not set(
                    map(int, bom.property_ids or [])) - set(properties or []):
                if not properties or bom.property_ids:
                    return bom
                elif not bom_empty_prop:
                    bom_empty_prop = bom
        return bom_empty_prop


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    property_ids = fields.Many2many('mrp.bom.property', string='Properties')


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _get_properties(self, bom_line):
        so_model = self.env['sale.order']
        if self.procurement_group_id:
            so_name = self.procurement_group_id.name
            so = so_model.search([('name', '=', so_name)])
            if so:
                for line in so.order_line:
                    if line.product_id == self.product_id:
                        if bom_line.property_ids not in line.property_ids:
                            return True
        return False

    def _generate_raw_moves(self, exploded_lines):
        self.ensure_one()
        moves = self.env['stock.move']
        for bom_line, line_data in exploded_lines:
            properties_check = self._get_properties(bom_line)
            if properties_check:
                moves += self._generate_raw_move(bom_line, line_data)
                return moves
