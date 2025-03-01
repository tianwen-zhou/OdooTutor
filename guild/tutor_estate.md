Odoo "First UI" 教程解析
--------------------

这个教程是Odoo服务器框架101系列的第5部分，主要教导如何为之前创建的"academy"模块添加用户界面(UI)。

### 1\. 教程概述

这部分教程的主要目标是:

*   为之前创建的模块添加用户界面
*   学习Odoo的视图系统（Views System）
*   了解如何定义和使用不同类型的视图

### 2\. 视图定义

Odoo使用XML文件来定义视图。首先，我们需要创建一个新的XML文件来定义视图:

需要在`academy`模块下创建`views/academy_views.xml`，内容大致如下:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_academy_teachers" model="ir.actions.act_window">
        <field name="name">Academy teachers</field>
        <field name="res_model">academy.teachers</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="menu_academy" name="Academy"/>
    <menuitem id="menu_academy_sub" name="Academy" parent="menu_academy"/>
    <menuitem id="menu_academy_teachers" name="Teachers" parent="menu_academy_sub" action="action_academy_teachers"/>
</odoo>
```

这段代码做了以下几件事:

1.  定义了一个动作(`ir.actions.act_window`)，指定了要显示的模型和视图模式
2.  创建了菜单项，将动作连接到用户界面

### 3\. 更新`__manifest__.py`

接下来，需要更新模块的清单文件，让它知道新增的视图文件:

```python
{
    'name': "Academy",
    'summary': "Academy management module",
    'description': """
        This module helps managing an academy
    """,
    'author': "Me",
    'website': "http://www.example.com",
    'category': 'Education',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/academy_views.xml',
    ],
    'demo': [
    ],
}
```

主要变化是在`data`字段中添加了`views/academy_views.xml`。

### 4\. 视图类型

教程接下来解释了Odoo中的不同视图类型:

1.  **列表视图(List/Tree View)**: 以表格形式显示记录
2.  **表单视图(Form View)**: 用于创建和编辑单个记录
3.  **搜索视图(Search View)**: 用于定义可搜索和过滤的字段
4.  **其他视图**: 如看板(Kanban)、日历(Calendar)、透视表(Pivot)等

### 5\. 添加自定义视图

我们可以继续完善视图定义，添加自定义树形视图和表单视图:

```xml
<record id="view_academy_teachers_tree" model="ir.ui.view">
    <field name="name">academy.teachers.tree</field>
    <field name="model">academy.teachers</field>
    <field name="arch" type="xml">
        <tree string="Teachers">
            <field name="name"/>
            <field name="biography"/>
        </tree>
    </field>
</record>

<record id="view_academy_teachers_form" model="ir.ui.view">
    <field name="name">academy.teachers.form</field>
    <field name="model">academy.teachers</field>
    <field name="arch" type="xml">
        <form string="Teacher">
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="biography"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

这些定义分别创建了列表视图和表单视图，指定了要显示的字段。

### 6\. 安全访问规则

教程还提到了需要设置安全访问规则。要创建`security/ir.model.access.csv`文件，内容如下:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_academy_teachers,access_academy_teachers,model_academy_teachers,,1,1,1,1
```

这为所有用户提供了对`academy.teachers`模型的完全权限。

### 7\. 实践步骤

让我们总结一下实现该教程需要的步骤:

1.  创建`views/academy_views.xml`文件，定义动作和菜单
2.  添加自定义视图定义(树形视图和表单视图)
3.  更新`__manifest__.py`，添加视图文件到`data`列表
4.  创建`security/ir.model.access.csv`设置访问权限
5.  重启Odoo服务器并更新模块

### 8\. 模块结构

完成后，模块的文件结构应该是:

```
academy/
|-- __init__.py
|-- __manifest__.py
|-- models/
|   |-- __init__.py
|   |-- academy_models.py
|-- security/
|   |-- ir.model.access.csv
|-- views/
|   |-- academy_views.xml
```

你对这个教程有任何特定部分想要更深入了解吗？或者你在实现过程中遇到了什么问题？

## Response:
我来为你寻找Odoo的Real Estate Advertisement模块的完整例子。这个模块是Odoo官方教程中的一个非常详尽的示例项目，常用于学习Odoo开发。

Odoo官方有一个很好的Real Estate模块教程，这是在开发者文档中的综合案例。让我为你整理这个项目的完整结构和关键代码。

Odoo Real Estate Module 完整示例
----------------------------

这个模块通常命名为`estate`，用于管理房地产广告信息。以下是完整的项目结构和关键文件内容：

### 项目结构

```
estate/
|-- __init__.py
|-- __manifest__.py
|-- security/
|   |-- ir.model.access.csv
|-- models/
|   |-- __init__.py
|   |-- estate_property.py
|   |-- estate_property_type.py
|   |-- estate_property_tag.py
|   |-- estate_property_offer.py
|-- views/
|   |-- estate_property_views.xml
|   |-- estate_property_type_views.xml
|   |-- estate_property_tag_views.xml
|   |-- estate_property_offer_views.xml
|   |-- estate_menus.xml
|-- wizard/
|   |-- __init__.py
|   |-- estate_property_wizard.py
|-- report/
|   |-- estate_property_reports.xml
|   |-- estate_property_templates.xml
|-- data/
|   |-- estate_property_demo.xml
```

### 关键文件内容

#### 1\. `__init__.py`（根目录）

```python
from . import models
from . import wizard
```

#### 2\. `__manifest__.py`

```python
{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'sequence': -100,
    'summary': 'Real Estate Advertisement Management',
    'description': """
        This module allows you to manage real estate properties
        and their offers.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
        'wizard/estate_property_wizard.xml',
        'report/estate_property_reports.xml',
        'report/estate_property_templates.xml',
        'data/estate_property_sequence.xml',
    ],
    'demo': [
        'data/estate_property_demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
```

#### 3\. `models/__init__.py`

```python
from . import estate_property
from . import estate_property_type
from . import estate_property_tag
from . import estate_property_offer
```

#### 4\. `models/estate_property.py`

```python
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
        tracking=True
    )
    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped('price')) if prop.offer_ids else 0.0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def action_sold(self):
        for prop in self:
            if prop.state == 'canceled':
                raise UserError(_("Canceled properties cannot be sold."))
            prop.state = 'sold'
        return True
    
    def action_cancel(self):
        for prop in self:
            if prop.state == 'sold':
                raise UserError(_("Sold properties cannot be canceled."))
            prop.state = 'canceled'
        return True
    
    @api.constrains('expected_price', 'selling_price')
    def _check_price_difference(self):
        for prop in self:
            if not float_is_zero(prop.selling_price, precision_digits=2) and float_compare(prop.selling_price, prop.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price!"))
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive'),
    ]
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for prop in self:
            if prop.state not in ('new', 'canceled'):
                raise UserError(_("Only new and canceled properties can be deleted."))
```

#### 5\. `models/estate_property_type.py`

```python
from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    
    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=10)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer("Offer Count", compute="_compute_offer_count")
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for prop_type in self:
            prop_type.offer_count = len(prop_type.offer_ids)
```

#### 6\. `models/estate_property_tag.py`

```python
from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
    
    name = fields.Char("Name", required=True)
    color = fields.Integer("Color")
    
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique')
    ]
```

#### 7\. `models/estate_property_offer.py`

```python
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    
    price = fields.Float("Price", required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)
    
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + timedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
    
    def action_accept(self):
        for offer in self:
            if offer.property_id.state != 'new' and offer.property_id.state != 'offer_received':
                raise UserError(_("Property is not in a state to accept offers."))
            
            # Update related offers
            offers = self.env["estate.property.offer"].search([
                ("property_id", "=", offer.property_id.id),
                ("id", "!=", offer.id)
            ])
            offers.action_refuse()
            
            # Update property
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True
    
    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
    
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The price must be strictly positive')
    ]
    
    @api.model
    def create(self, vals):
        property_id = self.env["estate.property"].browse(vals['property_id'])
        
        # Check if offer price is lower than existing offers
        if property_id.offer_ids:
            max_offer = max(property_id.offer_ids.mapped('price'))
            if vals['price'] < max_offer:
                raise UserError(_("The offer must be higher than %.2f", max_offer))
        
        # Update property state
        property_id.state = 'offer_received'
        
        return super().create(vals)
```

#### 8\. `views/estate_property_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Tree View -->
    <record id="estate_property_view_tree" model="ir.ui.view">
        <field name="name">estate.property.tree</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <tree string="Properties">
                <field name="name"/>
                <field name="property_type_id"/>
                <field name="postcode"/>
                <field name="bedrooms"/>
                <field name="living_area"/>
                <field name="expected_price"/>
                <field name="selling_price"/>
                <field name="date_availability"/>
                <field name="state" decoration-success="state == 'offer_accepted'" decoration-info="state == 'offer_received'" decoration-danger="state == 'canceled'" decoration-bf="state == 'sold'"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="estate_property_view_form" model="ir.ui.view">
        <field name="name">estate.property.form</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <form string="Property">
                <header>
                    <button name="action_sold" type="object" string="Sold" states="offer_accepted" class="oe_highlight"/>
                    <button name="action_cancel" type="object" string="Cancel" states="new,offer_received,offer_accepted"/>
                    <field name="state" widget="statusbar" statusbar_visible="new,offer_received,offer_accepted,sold"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name"/>
                        </h1>
                        <field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
                    </div>
                    <group>
                        <group>
                            <field name="property_type_id"/>
                            <field name="postcode"/>
                            <field name="date_availability"/>
                        </group>
                        <group>
                            <field name="expected_price"/>
                            <field name="best_price"/>
                            <field name="selling_price"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description">
                            <group>
                                <group>
                                    <field name="description"/>
                                    <field name="bedrooms"/>
                                    <field name="living_area"/>
                                    <field name="facades"/>
                                    <field name="garage"/>
                                    <field name="garden"/>
                                    <field name="garden_area" attrs="{'invisible': [('garden', '=', False)]}"/>
                                    <field name="garden_orientation" attrs="{'invisible': [('garden', '=', False)]}"/>
                                    <field name="total_area"/>
                                </group>
                            </group>
                        </page>
                        <page string="Offers">
                            <field name="offer_ids" attrs="{'readonly': [('state', 'in', ('offer_accepted', 'sold', 'canceled'))]}">
                                <tree string="Offers" editable="bottom" decoration-success="status == 'accepted'" decoration-danger="status == 'refused'">
                                    <field name="price"/>
                                    <field name="partner_id"/>
                                    <field name="validity"/>
                                    <field name="date_deadline"/>
                                    <field name="status"/>
                                    <button name="action_accept" type="object" icon="fa-check" attrs="{'invisible': [('status', '!=', False)]}"/>
                                    <button name="action_refuse" type="object" icon="fa-times" attrs="{'invisible': [('status', '!=', False)]}"/>
                                </tree>
                            </field>
                        </page>
                        <page string="Other Info">
                            <group>
                                <group>
                                    <field name="salesperson_id"/>
                                    <field name="buyer_id" attrs="{'invisible': [('buyer_id', '=', False)]}"/>
                                </group>
                            </group>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids" widget="mail_followers"/>
                    <field name="activity_ids" widget="mail_activity"/>
                    <field name="message_ids" widget="mail_thread"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="estate_property_view_search" model="ir.ui.view">
        <field name="name">estate.property.search</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <search string="Properties">
                <field name="name"/>
                <field name="property_type_id"/>
                <field name="postcode"/>
                <field name="expected_price"/>
                <field name="bedrooms"/>
                <field name="living_area"/>
                <field name="facades"/>
                <field name="tag_ids"/>
                <separator/>
                <filter string="Available" name="available" domain="[('state', 'in', ('new', 'offer_received'))]"/>
                <group expand="1" string="Group By">
                    <filter string="Status" name="state" context="{'group_by':'state'}"/>
                    <filter string="Property Type" name="property_type_id" context="{'group_by':'property_type_id'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Kanban View -->
    <record id="estate_property_view_kanban" model="ir.ui.view">
        <field name="name">estate.property.kanban</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <kanban default_group_by="state">
                <field name="state"/>
                <field name="name"/>
                <field name="property_type_id"/>
                <field name="expected_price"/>
                <field name="selling_price"/>
                <field name="tag_ids"/>
                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_global_click">
                            <div class="oe_kanban_details">
                                <strong class="o_kanban_record_title">
                                    <field name="name"/>
                                </strong>
                                <div>
                                    <field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
                                </div>
                                <div>
                                    <strong>Type: </strong>
                                    <field name="property_type_id"/>
                                </div>
                                <div>
                                    <strong>Expected Price: </strong>
                                    <field name="expected_price" widget="monetary"/>
                                </div>
                                <div t-if="record.selling_price.raw_value > 0">
                                    <strong>Selling Price: </strong>
                                    <field name="selling_price" widget="monetary"/>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Actions -->
    <record id="estate_property_action" model="ir.actions.act_window">
        <field name="name">Properties</field>
        <field name="res_model">estate.property</field>
        <field name="view_mode">kanban,tree,form</field>
        <field name="context">{'search_default_available': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create a property
            </p>
            <p>
                Create real estate properties to sell or rent.
            </p>
        </field>
    </record>
</odoo>
```

#### 9\. `views/estate_menus.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="estate_menu_root" name="Real Estate">
        <menuitem id="estate_first_level_menu" name="Advertisements">
            <menuitem id="estate_property_menu_action" action="estate_property_action" sequence="10"/>
            <menuitem id="estate_property_type_menu_action" action="estate_property_type_action" sequence="20"/>
        </menuitem>
        <menuitem id="estate_second_level_menu" name="Settings">
            <menuitem id="estate_property_tag_menu_action" action="estate_property_tag_action" sequence="10"/>
        </menuitem>
        <menuitem id="estate_reports_menu" name="Reports">
            <menuitem id="estate_property_report_menu" action="estate_property_report_action" sequence="10"/>
        </menuitem>
    </menuitem>
</odoo>
```

#### 10\. `security/ir.model.access.csv`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property,access.estate.property,model_estate_property,base.group_user,1,1,1,1
access_estate_property_type,access.estate.property.type,model_estate_property_type,base.group_user,1,1,1,1
access_estate_property_tag,access.estate.property.tag,model_estate_property_tag,base.group_user,1,1,1,1
access_estate_property_offer,access.estate.property.offer,model_estate_property_offer,base.group_user,1,1,1,1
```

#### 11\. `data/estate_property_sequence.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_estate_property" model="ir.sequence">
            <field name="name">Property Sequence</field>
            <field name="code">estate.property</field>
            <field name="prefix">PR</field>
            <field name="padding">5</field>
            <field name="company_id" eval="False"/>
        </record>
    </data>
</odoo>
```

### 高级功能扩展

以下是一些可以添加到基础模块中的高级特性：

#### 1\. `wizard/estate_property_wizard.py`

```python
from odoo import api, fields, models

class EstatePropertyWizard(models.TransientModel):
    _name = "estate.property.wizard"
    _description = "Create Offer for Selected Properties"
    
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    price = fields.Float("Price", required=True)
    
    def action_make_offer(self):
        property_ids = self.env.context.get('active_ids', [])
        for property_id in property_ids:
            self.env['estate.property.offer'].create({
                'property_id': property_id,
                'partner_id': self.partner_id.id,
                'price': self.price,
            })
        return True
```

#### 2\. `wizard/estate_property_wizard.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="estate_property_wizard_form" model="ir.ui.view">
        <field name="name">estate.property.wizard.form</field>
        <field name="model">estate.property.wizard</field>
        <field name="arch" type="xml">
            <form string="Create an Offer">
                <group>
                    <field name="partner_id"/>
                    <field name="price"/>
                </group>
                <footer>
                    <button name="action_make_offer" string="Create Offer" type="object" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>
    
    <record id="action_estate_property_wizard" model="ir.actions.act_window">
        <field name="name">Create Offer</field>
        <field name="res_model">estate.property.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
        <field name="binding_model_id" ref="model_estate_property"/>
        <field name="binding_view_types">list,form</field>
    </record>
</odoo>
```

#### 3\. `report/estate_property_reports.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="estate_property_report_action" model="ir.actions.report">
        <field name="name">Property Report</field>
        <field name="model">estate.property</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">estate.report_property_template</field>
        <field name="report_file">estate.report_property</field>
        <field name="binding_model_id" ref="model_estate_property"/>
        <field name="binding_type">report</field>
    </record>
</odoo>
```

#### 4\. `report/estate_property_templates.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_property_template">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="property">
                <t t-call="web.external_layout">
                    <div class="page">
                        <h2 t-field="property.name"/>
                        <div class="row mt32 mb32">
                            <div class="col-6">
                                <strong>Property Type:</strong>
                                <span t-field="property.property_type_id"/>
                                <br/>
                                <strong>Postcode:</strong>
                                <span t-field="property.postcode"/>
                                <br/>
                                <strong>Available From:</strong>
                                <span t-field="property.date_availability"/>
                            </div>
                            <div class="col-6">
                                <strong>Expected Price:</strong>
                                <span t-field="property.expected_price"/>
                                <br/>
                                <strong>Selling Price:</strong>
                                <span t-field="property.selling_price"/>
                                <br/>
                                <strong>Status:</strong>
                                <span t-field="property.state"/>
                            </div>
                        </div>
                        <h3>Description</h3>
                        <p t-field="property.description"/>
                        <div class="row">
                            <div class="col-6">
                                <strong>Bedrooms:</strong>
                                <span t-field="property.bedrooms"/>
                                <br/>
                                <strong>Living Area:</strong>
                                <span t-field="property.living_area"/> sqm
                            </div>
                            <div class="col-6">
                                <strong>Total Area:</strong>
                                <span t-field="property.total_area"/> sqm
                                <br/>
                                <strong>Facades:</strong>
                                <span t-field="property.facades"/>
                            </div>
                        </div>
                        <h3 t-if="property.offer_ids">Offers</h3>
                        <table class="table table-sm" t-if="property.offer_ids">
                            <thead>
                                <tr>
                                    <th>Price</th>
                                    <th>Partner</th>
                                    <th>Status</th>
                                    <th>Deadline</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr t-foreach="property.offer_ids" t-as="offer">
                                    <td t-field="offer.price"/>
                                    <td t-field="offer.partner_id"/>
                                    <td t-field="offer.status"/>
                                    <td t-field="offer.date_deadline"/>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>
```

这个完整示例包含了Odoo房地产模块的所有主要组件：模型定义、视图、动作、菜单、向导、报表等。该示例展示了Odoo开发的许多核心概念，包括：

1.  数据模型和字段类型
2.  关系字段（Many2one, One2many, Many2many）
3.  计算字段和存储
4.  约束和SQL约束
5.  状态管理和工作流
6.  各种类型的视图（表单、列表、看板等）
7.  向导（弹出式窗口）
8.  报表输出
9.  安全访问规则

这个示例对于学习Odoo开发非常有帮助，你可以根据需要修改和扩展它。


