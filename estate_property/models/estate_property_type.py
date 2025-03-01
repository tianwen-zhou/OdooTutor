from odoo import models, fields, api

class EstateAdPropertyType(models.Model): 
    _name = 'estatead.property.type'
    _description = 'EstateAD Property Type'
    _order = "name"

    name = fields.Char(required=True)
    # 以下两个字段不会在数据库中存储，只是用来显示，需要存的话需要加store=True
    property_ids = fields.One2many('estatead.property', 'property_type_id', string='Properties')
    property_count = fields.Integer(compute='_compute_property_count')
    sequence = fields.Integer('Sequence', default=10, help="Used to order property types. Lower is better.")
    # 在 estate.property.type 模型中添加
    offer_ids = fields.One2many('estatead.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count')

    @api.depends('property_ids')
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)    

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)