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
```python
