# Odoo POS 系统自定义字段完整指南

**生成日期:** 2023-05-08 23:46:34 UTC  
**作者:** tianwen-zhou

## 目录

1. [概述](#概述)
2. [字段定义](#字段定义)
3. [字段保存到数据库](#字段保存到数据库)
4. [加载字段到前端上下文](#加载字段到前端上下文)
5. [在收据上打印字段](#在收据上打印字段)
6. [最佳实践与常见问题](#最佳实践与常见问题)

## 概述

Odoo POS系统中处理订单(pos.order)和支付(pos.payment)的自定义字段需要考虑完整的数据流程：

前端UI → 数据库存储 → 历史订单加载 → 界面显示/收据打印


本文档以支付终端(Windcave)集成为例，展示从字段定义到前端显示的全流程实现。

## 字段定义

### 支付模型扩展

```python
# models/pos_payment.py
from odoo import api, fields, models

class PosPayment(models.Model):
    _inherit = 'pos.payment'
    
    # 定义支付相关字段
    windcave_dps_txn_ref = fields.Char('Windcave DPS Transaction Reference')
    windcave_txn_ref = fields.Char('POS Transaction Reference')
    windcave_auth_code = fields.Char('Authorization Code')
    windcave_cashback_amount = fields.Float('Cashback Amount', digits='Product Price')
    windcave_receipt_data = fields.Text('Windcave Receipt Data')

### 订单模型扩展
# models/pos_order.py
from odoo import api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    # 订单层面的必要字段
    windcave_dps_txn_ref = fields.Char('Windcave Reference',
                                     help="Stored for quick reference and reporting")

# 字段保存到数据库
# 支付字段映射

# models/pos_order.py
@api.model
def _payment_fields(self, order, ui_paymentline):
    """将前端支付数据映射到字段"""
    fields = super()._payment_fields(order, ui_paymentline)
    
    # 添加Windcave字段
    if ui_paymentline.get('windcave_dps_txn_ref'):
        fields.update({
            'windcave_dps_txn_ref': ui_paymentline.get('windcave_dps_txn_ref'),
            'windcave_txn_ref': ui_paymentline.get('windcave_txn_ref'),
            'windcave_auth_code': ui_paymentline.get('windcave_auth_code'),
            'windcave_cashback_amount': ui_paymentline.get('windcave_cashback_amount', 0.0),
            'windcave_receipt_data': ui_paymentline.get('windcave_receipt_data'),
        })
    
    return fields

#订单字段映射
# models/pos_order.py
@api.model
def _order_fields(self, ui_order):
    """将前端订单数据映射到字段"""
    fields = super()._order_fields(ui_order)
    
    # 从订单直接获取
    if ui_order.get('windcave_dps_txn_ref'):
        fields['windcave_dps_txn_ref'] = ui_order.get('windcave_dps_txn_ref')
    # 或从支付行获取
    elif ui_order.get('statement_ids'):
        for statement in ui_order.get('statement_ids'):
            if len(statement) > 2 and statement[2].get('windcave_dps_txn_ref'):
                fields['windcave_dps_txn_ref'] = statement[2].get('windcave_dps_txn_ref')
                break
    
    return fields

##支付处理钩子
# models/pos_order.py
@api.model
def _process_payment_lines(self, pos_order, order, pos_session, draft):
    """处理支付行后回填订单字段"""
    result = super()._process_payment_lines(pos_order, order, pos_session, draft)
    
    # 如果有Windcave支付，更新订单字段
    for payment in order.payment_ids:
        if payment.windcave_dps_txn_ref:
            order.write({
                'windcave_dps_txn_ref': payment.windcave_dps_txn_ref
            })
            break
            
    return result

##支付模型导出方法
# models/pos_payment.py
def _export_for_ui(self, payment):
    """支付记录导出到前端"""
    result = super()._export_for_ui(payment)
    
    # 添加所有自定义字段
    result.update({
        'windcave_dps_txn_ref': payment.windcave_dps_txn_ref,
        'windcave_txn_ref': payment.windcave_txn_ref,
        'windcave_auth_code': payment.windcave_auth_code,
        'windcave_cashback_amount': payment.windcave_cashback_amount,
        'windcave_receipt_data': payment.windcave_receipt_data,
    })
    
    return result

##订单模型导出方法
# models/pos_order.py
@api.model
def _export_for_ui(self, order):
    """订单记录导出到前端"""
    result = super()._export_for_ui(order)
    
    # 添加订单级字段
    result['windcave_dps_txn_ref'] = order.windcave_dps_txn_ref
    
    return result

## 前端数据处理
// static/src/js/models.js
patch(Order.prototype, {
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        // 加载订单级字段
        if (json.windcave_dps_txn_ref) {
            this.windcave_dps_txn_ref = json.windcave_dps_txn_ref;
        }
    },
    
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        // 导出订单级字段
        if (this.windcave_dps_txn_ref) {
            json.windcave_dps_txn_ref = this.windcave_dps_txn_ref;
        }
        return json;
    }
});

patch(Payment.prototype, {
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        // 加载支付行字段
        if (json.windcave_dps_txn_ref) {
            this.windcave_dps_txn_ref = json.windcave_dps_txn_ref;
        }
        if (json.windcave_receipt_data) {
            this.windcave_receipt_data = json.windcave_receipt_data;
        }
        // 其他字段...
    },
    
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        // 导出支付行字段
        if (this.windcave_dps_txn_ref) {
            json.windcave_dps_txn_ref = this.windcave_dps_txn_ref;
        }
        // 其他字段...
        return json;
    }
});
```

在收据上打印字段
