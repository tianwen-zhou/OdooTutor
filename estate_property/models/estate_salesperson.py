from odoo import models, fields, api

class EstatePropertySalesPerson(models.Model):
    _inherit = 'res.users'
    _description = 'Estate Sales Person'

    property_ids = fields.One2many('estatead.property', 'seller_id', string='Properties',domain=[('state', '!=', 'canceled')])
    property_count = fields.Integer(compute='_compute_property_count')

    @api.depends('property_ids') 
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)
    