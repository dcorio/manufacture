# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MrpPropertyGroup(models.Model):
    _name = 'mrp.property.group'
    _description = 'Property Group'

    name = fields.Char('Property Group', required=True)
    description = fields.Text('Description')


class MrpProperty(models.Model):
    _name = 'mrp.property'
    _description = 'Property'

    name = fields.Char('Name', required=True),
    group_id = fields.Many2one(
        'mrp.property.group', 'Property Group', required=True),
    description = fields.Text('Description')


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    property_ids = fields.Many2many('mrp.property', string='Properties')
