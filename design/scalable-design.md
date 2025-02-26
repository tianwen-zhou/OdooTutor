# Odoo 的灵活扩展机制

Odoo 设计了一套全面的扩展机制，使开发者能够在不修改核心代码的情况下扩展和定制系统功能。这种设计理念使 Odoo 成为一个高度可扩展的企业应用平台。以下是 Odoo 实现灵活扩展的主要机制：

## 一、模块化架构

Odoo 采用模块化架构，所有功能都通过模块实现，这是灵活扩展的基础。

### 1. 模块结构

一个典型的 Odoo 模块包含以下结构：

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
├── views/
├── security/
├── data/
├── static/
└── controllers/
```

### 2. 模块依赖

通过在 `__manifest__.py` 中定义依赖关系，模块可以在其他模块基础上构建功能：

```python
{
    'name': '高级销售',
    'version': '1.0',
    'depends': ['sale', 'stock'],
    'data': [
        'views/sale_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
```

## 二、模型继承机制

Odoo 提供了三种模型继承机制，使开发者能够扩展现有模型。

### 1. 传统继承 (Classical Inheritance)

用于扩展现有模型，添加新字段或方法：

```python
from odoo import models, fields

class SaleOrderExtended(models.Model):
    _inherit = 'sale.order'
    
    approval_state = fields.Selection([
        ('pending', '待审批'),
        ('approved', '已审批'),
        ('rejected', '已拒绝')
    ], string='审批状态', default='pending')
    
    def action_approve(self):
        self.write({'approval_state': 'approved'})
```

### 2. 委托继承 (Delegation Inheritance)

用于实现类似于多继承的功能，通过委托字段关联另一个模型：

```python
from odoo import models, fields

class EmployeeDocument(models.Model):
    _name = 'hr.employee.document'
    
    name = fields.Char('文档名称')
    document_type = fields.Selection([
        ('passport', '护照'),
        ('id_card', '身份证'),
        ('certificate', '证书')
    ])
    issue_date = fields.Date('签发日期')
    expiry_date = fields.Date('过期日期')

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    document_id = fields.Many2one('hr.employee.document')
    # 委托继承
    _inherits = {'hr.employee.document': 'document_id'}
```

### 3. 原型继承 (Prototype Inheritance)

用于创建一个新模型，该模型继承另一个模型的所有特性：

```python
from odoo import models, fields

class EmployeeContractor(models.Model):
    _name = 'hr.employee.contractor'
    _inherit = 'hr.employee'  # 原型继承
    
    contract_company = fields.Char('合同公司')
    contract_start = fields.Date('合同开始日期')
    contract_end = fields.Date('合同结束日期')
```

## 三、视图继承与扩展

Odoo 允许扩展现有视图，添加、修改或移除元素。

### 1. 视图继承

通过 XPath 或标识符定位视图元素，然后进行修改：

```xml
<record id="view_sale_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <!-- 在特定位置添加字段 -->
        <field name="partner_id" position="after">
            <field name="approval_state" widget="badge"/>
        </field>
        
        <!-- 使用 XPath 定位并修改元素 -->
        <xpath expr="//notebook" position="inside">
            <page string="审批信息">
                <group>
                    <field name="approver_id"/>
                    <field name="approval_date"/>
                    <field name="approval_notes"/>
                </group>
            </page>
        </xpath>
        
        <!-- 修改按钮属性 -->
        <button name="action_confirm" position="attributes">
            <attribute name="attrs">{'invisible': [('approval_state', '!=', 'approved')]}</attribute>
        </button>
    </field>
</record>
```

### 2. QWeb 模板继承

扩展网站模板和报表：

```xml
<template id="product_item_extended" inherit_id="website_sale.products_item">
    <xpath expr="//div[hasclass('product_price')]" position="after">
        <div t-if="product.inventory_availability == 'out_of_stock'" class="text-danger">
            <i class="fa fa-times-circle"/> 缺货
        </div>
        <div t-elif="product.qty_available &lt;= product.low_stock_threshold" class="text-warning">
            <i class="fa fa-exclamation-triangle"/> 库存不足
        </div>
    </xpath>
</template>
```

## 四、重写业务逻辑

通过继承和重写方法，可以修改或扩展业务逻辑。

### 1. 方法重写

完全替换原有方法的实现：

```python
from odoo import models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    def button_confirm(self):
        # 自定义确认逻辑
        for order in self:
            if order.amount_total > 10000 and not order.approval_id:
                return order.action_create_approval_request()
        # 调用原始方法
        return super(PurchaseOrder, self).button_confirm()
```

### 2. 方法扩展

通过装饰器在原方法前后添加逻辑：

```python
from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.model
    def create(self, vals):
        # 创建前处理
        if 'client_order_ref' not in vals:
            vals['client_order_ref'] = self.env['ir.sequence'].next_by_code('client.order.reference')
        
        # 调用原始方法
        result = super(SaleOrder, self).create(vals)
        
        # 创建后处理
        result.message_post(body="销售订单已创建，等待审批")
        
        return result
```

## 五、钩子系统

Odoo 提供多种钩子方法，允许在特定事件发生时执行自定义代码。

### 1. ORM 钩子

```python
from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    @api.model_create_multi
    def create(self, vals_list):
        # 创建前处理
        return super(ProductProduct, self).create(vals_list)
    
    def write(self, vals):
        # 写入前处理
        return super(ProductProduct, self).write(vals)
    
    def unlink(self):
        # 删除前处理
        return super(ProductProduct, self).unlink()
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        # 自定义搜索逻辑
        return super(ProductProduct, self)._name_search(name, args, operator, limit, name_get_uid)
```

### 2. 业务流程钩子

```python
from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def button_validate(self):
        # 自定义验证逻辑
        return super(StockPicking, self).button_validate()
    
    def _action_done(self):
        # 在完成操作时执行
        result = super(StockPicking, self)._action_done()
        # 完成后处理
        return result
```

## 六、服务器动作和自动化

Odoo 提供了无代码/低代码的扩展机制。

### 1. 服务器动作 (Server Actions)

通过 UI 配置的服务器端操作：

```xml
<record id="action_send_approval_reminder" model="ir.actions.server">
    <field name="name">发送审批提醒</field>
    <field name="model_id" ref="model_purchase_order"/>
    <field name="binding_model_id" ref="model_purchase_order"/>
    <field name="state">code</field>
    <field name="code">
for record in records:
    if record.state == 'to approve' and (datetime.now() - record.date_order).days > 3:
        template = env.ref('purchase.email_template_approval_reminder')
        template.send_mail(record.id, force_send=True)
    </field>
</record>
```

### 2. 自动化规则 (Automated Actions)

基于触发器的自动处理：

```xml
<record id="rule_auto_validate_small_po" model="base.automation">
    <field name="name">自动确认小额采购单</field>
    <field name="model_id" ref="model_purchase_order"/>
    <field name="trigger">on_create_or_write</field>
    <field name="filter_domain">[('amount_total', '&lt;', 1000), ('state', '=', 'draft')]</field>
    <field name="state">code</field>
    <field name="code">
record.button_confirm()
    </field>
</record>
```

## 七、前端扩展机制

Odoo 提供了扩展和定制前端界面的机制。

### 1. JavaScript 继承

扩展现有的 JavaScript 组件：

```javascript
odoo.define('my_module.ProductKanbanRecord', function (require) {
"use strict";

var KanbanRecord = require('web.KanbanRecord');

var ProductKanbanRecord = KanbanRecord.extend({
    // 重写方法
    _openRecord: function () {
        if (this.modelName === 'product.product' && this.recordData.type === 'service') {
            // 自定义服务类产品的打开行为
            this._rpc({
                model: 'product.product',
                method: 'get_service_details',
                args: [this.id],
            }).then(function (result) {
                // 处理结果
            });
            return;
        }
        // 否则使用默认行为
        return this._super.apply(this, arguments);
    },
});

return ProductKanbanRecord;
});
```

### 2. Widget 扩展

创建自定义控件：

```javascript
odoo.define('my_module.ProgressBarWidget', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var fieldRegistry = require('web.field_registry');

var ProgressBarWidget = AbstractField.extend({
    template: 'ProgressBar',
    
    _render: function () {
        // 渲染进度条
        var value = this.value || 0;
        this.$el.html($('<div>', {
            class: 'progress',
        }).append($('<div>', {
            class: 'progress-bar',
            style: 'width: ' + value + '%',
            text: value + '%',
        })));
    },
});

fieldRegistry.add('progress_bar', ProgressBarWidget);

return ProgressBarWidget;
});
```

### 3. 资产扩展 (Assets Bundle)

添加或替换 CSS 和 JavaScript 资源：

```xml
<template id="assets_backend" inherit_id="web.assets_backend">
    <xpath expr="." position="inside">
        <link rel="stylesheet" href="/my_module/static/src/scss/my_style.scss"/>
        <script type="text/javascript" src="/my_module/static/src/js/my_widget.js"/>
    </xpath>
</template>
```

## 八、Web 控制器扩展

通过 HTTP 控制器扩展 Web 功能。

### 1. 控制器继承

```python
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleExtended(WebsiteSale):
    @http.route()
    def cart(self, **post):
        # 扩展购物车页面逻辑
        response = super(WebsiteSaleExtended, self).cart(**post)
        # 添加额外数据
        if response.qcontext:
            response.qcontext['recommended_products'] = request.env['product.product'].get_recommended()
        return response
    
    @http.route(['/shop/checkout/custom'], type='http', auth="public", website=True)
    def custom_checkout(self, **post):
        # 全新的自定义结账页面
        return request.render("my_module.custom_checkout_template", {
            'custom_data': self._prepare_custom_checkout_data(),
        })
```

## 九、数据导入和导出接口

Odoo 提供标准化的数据交换机制。

### 1. 数据文件

通过 XML 或 CSV 文件导入初始数据或配置：

```xml
<record id="custom_pricelist_rule" model="product.pricelist.item">
    <field name="pricelist_id" ref="product.list0"/>
    <field name="applied_on">1_product</field>
    <field name="product_tmpl_id" ref="product.product_product_4_product_template"/>
    <field name="compute_price">fixed</field>
    <field name="fixed_price">999.99</field>
</record>
```

### 2. 外部 API

通过 XML-RPC 或 JSON-RPC 进行系统集成：

```python
import xmlrpc.client

url = 'http://localhost:8069'
db = 'mydatabase'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
partners = models.execute_kw(db, uid, password, 'res.partner', 'search_read', 
                           [[['is_company', '=', True]]], {'fields': ['name', 'email', 'phone']})
```

## 十、开发者工具

Odoo 提供了多种工具，简化扩展开发过程。

### 1. 开发者模式

启用额外的调试功能和视图编辑器。

### 2. 继承视图编辑器

通过 UI 直接编辑和创建视图继承。

### 3. 技术特性

查看模型字段、工作流、动作等技术细节。

## 总结

Odoo 的灵活扩展机制建立在其模块化架构和丰富的继承系统之上，允许开发者在不同层次上定制系统：

1. **数据层**：通过模型继承扩展数据结构
2. **业务逻辑层**：通过方法重写定制业务流程
3. **表现层**：通过视图继承和前端扩展优化用户界面
4. **集成层**：通过控制器和 API 实现系统集成

这种灵活的扩展机制使 Odoo 能够适应各种业务需求，从简单的字段添加到复杂的流程重构，同时保持系统的可升级性和稳定性。