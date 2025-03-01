from odoo import models, fields, api

class EstateAdPropertyOffer(models.Model): 
    _name = 'estatead.property.offer'
    _description = 'EstateAD Property Offer'
    _order = "price desc"

    name = fields.Char()
    price = fields.Float(required=True) 
    offer_date = fields.Datetime(default=fields.Datetime.now)
    property_id = fields.Many2one('estatead.property', string='Property', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    validity = fields.Integer(default=7)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='draft', required=True)
    active = fields.Boolean(default=True)
    notes = fields.Text()
    # 以下两个字段不会在数据库中存储，只是用来显示，需要存的话需要加store=True
    property_name = fields.Char(related='property_id.name', string='Property Name', store=True)
    partner_name = fields.Char(related='partner_id.name', string='Partner Name', store=True)    
    property_type_id = fields.Many2one('estatead.property.type', related='property_id.property_type_id', string='Property Type', store=True)