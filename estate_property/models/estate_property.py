from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateADProperty(models.Model): 
    _name = 'estatead.property'
    _description = 'Estate Prperty'
    _order = "id desc"

    name = fields.Char(required=True, default='Unkonwn')
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    description = fields.Text()
    des_name = fields.Char(string='Description Name', compute='_compute_des_name', store=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    living_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_total_area', store=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)       
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True)
    best_price = fields.Float(readonly=True)
    property_type_id = fields.Many2one('estatead.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estatead.property.tag', string='Tags')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string='Seller')
    property_offer_ids = fields.One2many('estatead.property.offer', 'property_id', string='Offers')
    
    _sql_constraints = [
        ('check_bedrooms', 'CHECK(bedrooms >= 1 AND bedrooms <= 7)',
         'The bedrooms of an analytic distribution should be between 1 and 7.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('name')
    def _compute_des_name(self):
        for record in self:
            record.des_name = "Description for %s " % record.name

    @api.onchange('expected_price', 'selling_price')
    def _onchange_price(self):
        if self.expected_price < self.selling_price:
            self.best_price = self.expected_price
        else:
            self.best_price = self.selling_price

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 50
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
        
    def action_sold(self):
        self.state = 'sold'
        # self.active = False
        return True
    
    def action_cancel(self):
        self.state = 'canceled'
        # self.active = False
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price <= 0:
                raise ValidationError('The selling price must be positive')

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError('The expected price must be positive')
            
    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for record in self:
            if record.bedrooms <= 0:
                raise ValidationError('The number of bedrooms must be positive')

    @api.model 
    def create(self, vals):
        if vals.get('expected_price') < 0:
            raise ValidationError('The expected price must be positive')
        return super(EstateADProperty, self).create(vals)   
    
    # same as above but with _unlink_except_* as method name
    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_property(self):
        if any(property.state not in ['new', 'canceled'] for property in self):
            raise ValidationError("Can't delete an active property!!")

    # @api.ondelete(at_uninstall=False)
    # def _unlink_except_active_property(self):
    #     """ Prevent deletion of properties that are not in 'new' or 'canceled' state. """
    #     for property in self:
    #         if property.state not in ['new', 'canceled']:
    #             raise ValidationError("Can't delete an active property!")
