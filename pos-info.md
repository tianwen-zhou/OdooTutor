# Odoo Point of Sale 详细分析

## 1. 概述

Odoo Point of Sale (POS) 是Odoo套件中的销售点模块，提供了一个完整的零售解决方案，包括销售、库存管理、付款处理等功能。它的设计允许在在线和离线模式下运行，特别适合零售环境。

## 2. 架构分析

Odoo POS采用了混合架构：

1. **后端**：使用Python编写，基于Odoo的ORM系统
2. **前端**：使用JavaScript (ES6)、QWeb模板和CSS开发
3. **数据同步**：采用IndexedDB进行本地存储，支持离线操作

### 2.1 核心组件

- **POS会话**：`pos.session` 模型，表示收银员的工作会话
- **POS订单**：`pos.order` 模型，存储交易记录
- **POS支付**：`pos.payment` 模型，管理付款方式和交易
- **POS配置**：`pos.config` 模型，存储POS终端的设置

## 3. 代码结构分析

```
addons/point_of_sale/
├── models/              # 后端Python模型
├── static/              # 前端资源
│   ├── src/
│   │   ├── js/         # JavaScript代码
│   │   │   ├── models.js       # 数据模型定义
│   │   │   ├── screens.js      # 界面屏幕定义
│   │   │   ├── popups.js       # 弹窗组件
│   │   │   ├── db.js           # 本地数据库管理
│   │   │   └── chrome.js       # UI框架元素
│   │   └── xml/        # QWeb XML模板
│   └── tests/          # 测试代码
├── views/              # 后端视图定义
└── data/               # 初始化数据
```

## 4. 关键代码分析

### 4.1 后端模型 (Python)

`pos_order.py` 的核心部分:

```python
class PosOrder(models.Model):
    _name = "pos.order"
    _description = "Point of Sale Orders"
    _order = "date_order desc, name desc, id desc"

    name = fields.Char(string='Order Ref', required=True, readonly=True, copy=False, default='/')
    date_order = fields.Datetime(string='Order Date', readonly=True, index=True, default=fields.Datetime.now)
    user_id = fields.Many2one(
        comodel_name='res.users', string='Responsible',
        help="Person who uses the cash register. It can be a reliever, a student or an interim employee.",
        default=lambda self: self.env.uid,
        states={'done': [('readonly', True)], 'invoiced': [('readonly', True)]},
    )
    
    # 创建发票方法示例
    def action_pos_order_invoice(self):
        Invoice = self.env['account.move']
        for order in self:
            # 创建发票逻辑
            invoice = Invoice.create({
                'partner_id': order.partner_id.id,
                'invoice_origin': order.name,
                'invoice_line_ids': [(0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.qty,
                    'price_unit': line.price_unit,
                }) for line in order.lines],
            })
            order.write({'invoice_id': invoice.id, 'state': 'invoiced'})
        return True
```

### 4.2 前端模型 (JavaScript)

`models.js` 的核心部分:

```javascript
odoo.define('point_of_sale.models', function (require) {
    "use strict";
    
    var PosModel = Backbone.Model.extend({
        initialize: function(session, attributes) {
            this.session = session;
            this.set('orders', new OrderCollection());
            this.set('selectedOrder', null);
            
            // 从服务器加载初始数据
            this.load_server_data();
        },
        
        load_server_data: function(){
            var self = this;
            return this._loadModels().then(function(){
                return self.after_load_server_data();
            });
        },
        
        // 产品添加到订单
        add_product: function(product, options){
            var order = this.get_order();
            order.add_product(product, options);
        }
    });
    
    // 订单模型
    var Order = Backbone.Model.extend({
        initialize: function(attributes,options){
            this.pos = options.pos;
            this.set_orderlines([]);
            this.set_paymentlines([]);
            this.selected_orderline = undefined;
            this.selected_paymentline = undefined;
            this.set('client',null);
        },
        
        // 添加产品行
        add_product: function(product, options){
            options = options || {};
            var line = this.get_orderline(product.id);
            
            if(line){
                line.set_quantity(line.get_quantity() + 1);
            }else{
                line = new Orderline({}, {pos: this.pos, order: this, product: product});
                this.orderlines.add(line);
            }
            this.trigger('change');
            return line;
        }
    });
});
```

### 4.3 前端界面 (QWeb XML)

`screens.xml` 的部分内容:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">
    
    <t t-name="ProductScreenWidget">
        <div class="product-screen screen">
            <div class="screen-content">
                <div class="leftpane">
                    <div class="orders"></div>
                </div>
                <div class="rightpane">
                    <div class="products-widget">
                        <div class="product-list-container">
                            <div class="product-list"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </t>
    
    <t t-name="OrderWidget">
        <div class="order-container">
            <div class="order">
                <div class="order-info">
                    <div class="customer-name" t-if="order.get_client()">
                        <t t-esc="order.get_client().name" />
                    </div>
                </div>
                <div class="orderlines">
                </div>
                <div class="summary">
                    <div class="total">
                        <t t-esc="order.get_total_with_tax()" />
                    </div>
                </div>
            </div>
        </div>
    </t>
    
</templates>
```

## 5. 主要扩展点

Odoo POS提供了多个扩展点，允许开发者定制和扩展功能。

### 5.1 产品屏幕扩展

```javascript
odoo.define('custom_module.custom_product_screen', function(require) {
    'use strict';
    
    var ProductScreenWidget = require('point_of_sale.screens').ProductScreenWidget;
    var gui = require('point_of_sale.gui');
    
    // 扩展产品屏幕
    ProductScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options);
            // 添加自定义初始化逻辑
        },
        
        // 重写或扩展方法
        show: function(){
            this._super();
            // 添加自定义显示逻辑
        },
        
        // 添加新方法
        custom_method: function(){
            // 自定义功能实现
        }
    });
});
```

### 5.2 添加自定义按钮

```javascript
odoo.define('custom_module.custom_buttons', function(require) {
    'use strict';
    
    var screens = require('point_of_sale.screens');
    
    screens.ActionpadWidget.include({
        renderElement: function() {
            this._super();
            var self = this;
            
            // 添加自定义按钮
            this.$('.actionpad').append(
                $('<button>', {
                    class: 'custom-button',
                    text: '自定义按钮',
                    click: function() {
                        self.custom_button_action();
                    }
                })
            );
        },
        
        custom_button_action: function() {
            // 按钮点击事件处理
            this.gui.show_popup('confirm', {
                'title': '自定义操作',
                'body': '这是一个自定义操作',
                'confirm': function() {
                    // 确认操作
                }
            });
        }
    });
});
```

### 5.3 新增付款方式

```python
# 后端Python代码
class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'
    
    def _get_payment_terminal_selection(self):
        selection = super()._get_payment_terminal_selection()
        return selection + [('custom', 'Custom Terminal')]
    
    custom_terminal_api_key = fields.Char("API Key")
```

```javascript
// 前端JavaScript代码
odoo.define('custom_module.payment', function(require) {
    'use strict';
    
    var models = require('point_of_sale.models');
    var PaymentCustomTerminal = require('custom_module.terminal');
    
    // 扩展支付方式
    models.register_payment_method('custom', PaymentCustomTerminal);
    
    // 自定义支付终端实现
    var PaymentCustomTerminal = core.Class.extend({
        init: function(pos, payment_method) {
            this.pos = pos;
            this.payment_method = payment_method;
            this.api_key = payment_method.custom_terminal_api_key;
        },
        
        // 发送支付请求
        send_payment_request: function(cid) {
            // 实现支付请求逻辑
            return new Promise(function(resolve, reject) {
                // API调用实现
            });
        }
    });
    
    return PaymentCustomTerminal;
});
```

### 5.4 扩展订单模型

```javascript
odoo.define('custom_module.models', function(require) {
    'use strict';
    
    var models = require('point_of_sale.models');
    
    // 扩展订单模型
    var OrderSuper = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attributes, options) {
            OrderSuper.initialize.apply(this, arguments);
            this.custom_field = '';
        },
        
        // 添加自定义方法
        set_custom_field: function(value) {
            this.custom_field = value;
            this.trigger('change', this);
        },
        
        get_custom_field: function() {
            return this.custom_field;
        },
        
        // 重写导出数据方法以包含自定义字段
        export_as_JSON: function() {
            var json = OrderSuper.export_as_JSON.apply(this, arguments);
            json.custom_field = this.custom_field;
            return json;
        }
    });
    
    // 扩展模型加载
    models.load_fields('product.product', ['custom_product_field']);
});
```

### 5.5 后端订单处理扩展

```python
class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    custom_field = fields.Char('Custom Field')
    
    @api.model
    def _order_fields(self, ui_order):
        order_fields = super()._order_fields(ui_order)
        order_fields['custom_field'] = ui_order.get('custom_field', '')
        return order_fields
    
    # 扩展确认订单方法
    def action_pos_order_paid(self):
        result = super().action_pos_order_paid()
        # 添加自定义处理逻辑
        for order in self:
            if order.custom_field:
                # 执行基于自定义字段的操作
                pass
        return result
```

## 6. 高级扩展技术

### 6.1 自定义屏幕

```javascript
odoo.define('custom_module.screens', function(require) {
    'use strict';
    
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    
    // 创建自定义屏幕
    var CustomScreen = screens.ScreenWidget.extend({
        template: 'CustomScreenWidget',
        
        init: function(parent, options) {
            this._super(parent, options);
            this.custom_data = {};
        },
        
        show: function() {
            var self = this;
            this._super();
            
            // 屏幕初始化逻辑
            this.$('.confirm-button').click(function() {
                self.confirm_action();
            });
            
            this.$('.cancel-button').click(function() {
                self.gui.back();
            });
        },
        
        confirm_action: function() {
            // 处理确认操作
            this.gui.back();
        }
    });
    gui.define_screen({name:'custom_screen', widget: CustomScreen});
    
    // 在其他地方调用此屏幕
    // this.gui.show_screen('custom_screen');
});
```

相应的QWeb模板:

```xml
<t t-name="CustomScreenWidget">
    <div class="custom-screen screen">
        <div class="screen-content">
            <h1>自定义屏幕</h1>
            <div class="custom-content">
                <!-- 自定义内容 -->
            </div>
            <div class="buttons">
                <button class="confirm-button">确认</button>
                <button class="cancel-button">取消</button>
            </div>
        </div>
    </div>
</t>
```

### 6.2 离线数据处理

```javascript
odoo.define('custom_module.db', function(require) {
    'use strict';
    
    var PosDB = require('point_of_sale.DB');
    
    // 扩展本地数据库
    PosDB.include({
        init: function(options) {
            this._super(options);
            this.custom_data = {};
        },
        
        // 添加自定义数据存储方法
        save_custom_data: function(key, data) {
            this.custom_data[key] = data;
            this.save('custom_data', this.custom_data);
        },
        
        // 获取自定义数据
        get_custom_data: function(key) {
            return this.custom_data[key];
        },
        
        // 加载数据
        load: function(db_name) {
            this._super(db_name);
            
            try {
                this.custom_data = this.load('custom_data') || {};
            } catch(err) {
                this.custom_data = {};
            }
        }
    });
});
```

### 6.3 自定义报表

```xml
<record id="custom_pos_report" model="ir.actions.report">
    <field name="name">自定义POS报表</field>
    <field name="model">pos.order</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">custom_module.custom_pos_report_template</field>
    <field name="report_file">custom_module.custom_pos_report_template</field>
    <field name="binding_model_id" ref="model_pos_order"/>
    <field name="binding_type">report</field>
</record>
```

相应的QWeb报表模板:

```xml
<template id="custom_pos_report_template">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2>POS订单报表</h2>
                    <div class="row">
                        <div class="col-6">
                            <strong>订单号:</strong> <span t-field="doc.name"/>
                        </div>
                        <div class="col-6">
                            <strong>日期:</strong> <span t-field="doc.date_order"/>
                        </div>
                    </div>
                    <!-- 更多报表内容 -->
                </div>
            </t>
        </t>
    </t>
</template>
```

## 7. 性能优化技巧

1. **减少网络请求**：批量加载数据，利用POS的预加载机制
   
   ```javascript
   // 扩展预加载数据
   models.load_models([{
       model: 'custom.model',
       fields: ['name', 'code', 'description'],
       domain: function(self){ return [['active', '=', true]]; },
       loaded: function(self, data){
           self.custom_data = data;
       }
   }]);
   ```

2. **优化本地索引**：为频繁查询的字段创建索引
   
   ```javascript
   // DB.js扩展
   init: function(){
       this._super();
       this.custom_index = {};
   },
   
   add_custom_items: function(items){
       for(var i = 0; i < items.length; i++){
           var item = items[i];
           this.custom_index[item.id] = item;
       }
   }
   ```

3. **使用DOM片段减少重绘**：
   
   ```javascript
   renderElement: function(){
       var self = this;
       this._super();
       
       var fragment = document.createDocumentFragment();
       this.data.forEach(function(item){
           var el = self._create_item_element(item);
           fragment.appendChild(el);
       });
       
       this.$('.items-container').append(fragment);
   }
   ```

## 8. 常见扩展场景

1. **自定义收据格式**
2. **集成外部支付设备**
3. **添加客户忠诚度程序**
4. **多货币支持**
5. **自定义折扣和促销规则**
6. **库存实时检查**
7. **员工权限控制**
8. **分销商渠道集成**

## 9. 结论

Odoo POS模块提供了一个灵活、可扩展的销售点解决方案，其架构设计使得开发者可以通过多种方式进行定制和扩展。关键扩展点包括模型扩展、界面定制、支付方式集成以及业务流程定制。掌握这些扩展技术，开发者可以根据特定业务需求打造专属的POS系统。
