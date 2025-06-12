# 📖 Odoo 权限控制体系概览

---

## 📌 核心概念

Odoo 权限体系以 **Group (角色)** 为核心，通过多层控制实现灵活的权限管理：

-   **Group**：类似 Role，管理一组权限和可见性。
    
-   **Model Access 权限**：对模型的 CRUD 权限控制。
    
-   **Record Rule**：模型记录行级权限控制。
    
-   **菜单、视图、按钮、字段**：通过 `groups` 属性控制可见性。
    
-   **业务逻辑代码级控制**：在 Python 中动态判断用户是否拥有某权限。
    

---

## 📌 权限控制维度

| 控制对象 | 控制方式 | 基于 Group | 说明 |
| --- | --- | --- | --- |
| 模型 (Model) 权限 | `ir.model.access.csv` + Record Rules | ✅ | CRUD 级别权限，行级权限通过 Record Rule 实现 |
| 菜单项 (Menu) 可见性 | `groups` 属性 | ✅ | 没权限的 Group 看不到对应菜单 |
| 页面视图 (Form/Tree) | `groups` 属性 | ✅ | 没权限的 Group 看不到视图或视图中某些字段 |
| 按钮 / 字段 | `groups` 属性 | ✅ | 控制按钮/字段是否可见、可编辑 |
| Action (动作/报表) | `groups` 属性 | ✅ | 没权限的 Group 看不到对应的操作按钮/入口 |
| **业务代码逻辑** | `self.env.user.has_group()`、`check_access_rights()`、`check_access_rule()` | ✅ | 代码层强制权限判断 |

---

## 📌 Group 本质说明

-   Odoo 中 **Group 就是 Role**，存储在 `res.groups` 表。
    
-   Group 可以控制多个模型、多个模块、多个菜单、多个动作。
    
-   **Group 与 addons 没有绑定关系**，而是按业务场景自由组合权限。
    

---

## 📌 Record Rule (行级权限)

用于限制用户对模型记录的行级访问权限，按 Group 配置，常见于数据隔离场景。

**示例**：

```xml
<record id="rule_product_user_own" model="ir.rule">
  <field name="name">User Own Products</field>
  <field name="model_id" ref="product.model_product_product"/>
  <field name="domain_force">[('create_uid', '=', user.id)]</field>
  <field name="groups" eval="[(4, ref('your_module.group_label_user'))]"/>
</record>
```

含义：只有记录创建人是当前用户，才有查看权限。

---

## 📌 代码级权限判断

在 Python 业务代码中，动态判断用户是否有某个 Group 权限。

**示例**：

```python
if not self.env.user.has_group('your_module.group_label_manager'):
    raise UserError("You don't have permission to perform this action.")
```

**模型权限校验**：

```python
self.check_access_rights('write')
self.check_access_rule('write')
```

---

## 📌 特殊说明：Group 与 Application

-   **res.groups** 表有一个 `category_id` 字段，表示该组所属的 Application（应用分类）。
    
-   应用分类 (`ir.module.category`) 只是为了在「设置 → 用户与公司 → 用户」界面中分组显示 Group，方便勾选和管理。
    
-   与 **addons 安装模块的 application 字段** 没有强制绑定关系。
    

---

## 📌 总结

👉 **Odoo 权限体系以 Group 为核心，结合模型访问权限、菜单/视图/按钮/字段控制、行级 Record Rule 和代码级权限判断，构建出灵活、多层次、可扩展的权限控制机制。**

---

## 📌 推荐实操模板

> 权限设计场景：

-   `group_label_manager`：标签模板管理权限
    
-   `group_label_user`：标签打印权限（使用既有模板）
    

**应用在：**

-   模型访问
    
-   Record Rule 行级控制
    
-   菜单可见性
    
-   按钮/字段/动作
    
-   业务逻辑代码检查
    

---
