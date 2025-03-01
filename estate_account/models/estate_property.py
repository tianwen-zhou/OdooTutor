# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo import Command

class EstateProperty(models.Model):
    _inherit = 'estatead.property'
    _description = 'estate_account.estate_account'

    # Add a new field to the estate_property model, to link it to an account.account
    def action_sold(self):
        res = super().action_sold()
         # 获取客户（买家）
        if not self.buyer_id:
            raise ValidationError(_("The property must have a buyer before selling."))
        
        # 创建发票（account.move）
        invoice_vals = {
            "partner_id": self.buyer_id.id,  # 客户
            "move_type": "out_invoice",  # 客户发票
            "journal_id": self.env["account.journal"].search([("type", "=", "sale")], limit=1).id,  # 选择销售日记账
            "invoice_line_ids": [
                Command.create({
                    "name": _("6%% commission on property sale"),  # 6% 销售佣金
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }),
                Command.create({
                    "name": _("Administrative fees"),  # 额外 100 管理费
                    "quantity": 1,
                    "price_unit": 100.00,
                }),
            ],
        }
        self.env["account.move"].create(invoice_vals)  # 创建发票
        return res