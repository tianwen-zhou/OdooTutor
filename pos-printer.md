在Odoo Point of Sale中新增打印机
=========================

在Odoo POS中添加一个新打印机涉及几个关键步骤。Odoo支持多种打印机类型，包括ESC/POS打印机、网络打印机和浏览器打印。下面是详细的配置和开发流程：

基本配置方法（无需开发）
------------

### 1\. 在POS配置中添加打印机

1.  进入 **销售点(Point of Sale)** > **配置(Configuration)** > **销售点(Point of Sale)**
2.  选择要配置的POS终端
3.  在配置页面找到 **硬件(Hardware)** 选项卡
4.  在 **打印机(Printers)** 部分，点击 **添加一行(Add a line)** 来添加新打印机
5.  填写打印机信息：
    *   **打印机名称(Printer Name)**：给打印机起一个名称
    *   **打印机类型(Printer Type)**：选择打印机类型（ESC/POS、网络打印机等）
    *   **IP地址(IP Address)**：如果是网络打印机，填写IP地址
    *   **其他参数**：根据打印机类型填写相关配置

### 2\. 配置打印规则

1.  在同一配置页面，可以配置哪些文档使用特定打印机
2.  例如，可以设置收据使用一台打印机，而订单小票使用另一台打印机

开发方法（需要自定义开发）
-------------

### 1\. 添加自定义打印机类型

如果需要支持特殊类型的打印机，需要扩展打印机驱动：

```javascript
odoo.define('custom_module.custom_printer', function (require) {
    'use strict';

    var core = require('web.core');
    var PrinterMixin = require('point_of_sale.Printer').PrinterMixin;

    // 创建自定义打印机类
    var CustomPrinter = core.Class.extend(PrinterMixin, {
        init: function(url){
            this.url = url;
            this.connection = null;
        },

        // 打开连接
        open: function(){
            var self = this;
            return new Promise(function(resolve, reject){
                // 实现连接逻辑
                try {
                    self.connection = new YourPrinterSDK(self.url);
                    self.connection.connect({
                        success: function(){ resolve(); },
                        error: function(error){ reject(error); }
                    });
                } catch(error) {
                    reject(error);
                }
            });
        },

        // 打印操作
        print: function(receipt){
            var self = this;
            if(!this.connection){
                return this.open().then(function(){
                    return self.print(receipt);
                });
            }

            return new Promise(function(resolve, reject){
                self.connection.print(receipt, {
                    success: function(){ resolve(); },
                    error: function(error){ reject(error); }
                });
            });
        },

        // 关闭连接
        close: function(){
            if(this.connection){
                this.connection.close();
                this.connection = null;
            }
        }
    });

    return CustomPrinter;
});
```

### 2\. 注册打印机类型

在POS模块中注册新的打印机类型：

```javascript
odoo.define('custom_module.models', function (require) {
    'use strict';

    var models = require('point_of_sale.models');
    var CustomPrinter = require('custom_module.custom_printer');

    // 注册打印机类型
    models.Printer.include({
        init: function(url){
            this._super(url);
            
            var protocol = url.split('://')[0];
            if(protocol === 'custom'){
                this.connection = new CustomPrinter(url);
            }
        }
    });
});
```

### 3\. 扩展后端模型以支持新打印机类型

```python
from odoo import models, fields, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    custom_printer_url = fields.Char(string='Custom Printer URL')
    use_custom_printer = fields.Boolean(string='Use Custom Printer')

    @api.model
    def _get_printer_options(self):
        options = super()._get_printer_options()
        options.append(('custom', 'Custom Printer'))
        return options
```

### 4\. 修改前端模板以显示新打印机设置

```xml
<record id="view_pos_config_form_inherit" model="ir.ui.view">
    <field name="name">pos.config.form.inherit</field>
    <field name="model">pos.config</field>
    <field name="inherit_id" ref="point_of_sale.pos_config_view_form"/>
    <field name="arch" type="xml">
        <xpath expr="//div[@id='printer_options']" position="inside">
            <div class="row mt16" attrs="{'invisible': [('printer_type', '!=', 'custom')]}">
                <label for="custom_printer_url" class="col-lg-3"/>
                <field name="custom_printer_url" class="col-lg-9"/>
            </div>
        </xpath>
    </field>
</record>
```

实现特定打印模板
--------

要为特定类型的打印任务创建自定义模板，可以：

```javascript
odoo.define('custom_module.receipt', function(require) {
    'use strict';

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;

    models.Order = models.Order.extend({
        // 重写收据打印方法
        export_for_printing: function(){
            var receipt = _super_order.export_for_printing.apply(this, arguments);
            
            // 添加自定义字段到收据
            receipt.custom_field = 'Custom Value';
            
            return receipt;
        }
    });
});
```

然后修改收据模板：

```xml
<t t-name="CustomReceiptTemplate">
    <receipt align="center" width="40">
        <line>
            <left>订单号:</left>
            <right><t t-esc="receipt.name"/></right>
        </line>
        <line>
            <left>日期:</left>
            <right><t t-esc="receipt.date.localestring"/></right>
        </line>
        <line>
            <left>自定义字段:</left>
            <right><t t-esc="receipt.custom_field"/></right>
        </line>
        <!-- 其他自定义内容 -->
    </receipt>
</t>
```

使用特定打印机打印特定内容
-------------

```javascript
// 在需要打印的地方
print_receipt: function() {
    var receipt = this.get_receipt_render_env();
    var printer = this.pos.printer_for_type('custom');
    
    if (printer) {
        printer.print_receipt(receipt);
    } else {
        // 回退到默认打印机
        this.pos.proxy.print_receipt(receipt);
    }
}
```

打印机异常处理
-------

```javascript
try {
    await printer.print_receipt(receipt);
    this.showTempScreen('ReceiptScreen');
} catch (error) {
    this.showPopup('ErrorPopup', {
        title: '打印错误',
        body: '无法连接到打印机。请检查打印机连接并重试。'
    });
    
    // 记录错误
    console.error('Printer error:', error);
}
```

以上步骤涵盖了在Odoo POS中添加新打印机的主要方法，无论是通过标准配置还是自定义开发。根据您的具体需求和打印机类型，可能需要调整部分代码实现。
