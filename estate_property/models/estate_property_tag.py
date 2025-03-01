from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = 'estatead.property.tag'
    _description = 'Estate Property Tag'   
    _order = "name"     

    name = fields.Char(required=True)   
    color = fields.Integer()
    property_ids = fields.Many2many('estatead.property', string='Properties')
    property_count = fields.Integer(compute='_compute_property_count')  