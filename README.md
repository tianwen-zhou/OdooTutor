# OdooTutor

# 命名
# `ir.actions.act_window.view` 解析

在 Odoo 中，**`ir`** 代表 **"Information Repository"（信息存储库）**，它是 Odoo 的一个核心命名空间，用于存储和管理通用的配置信息，如动作（Actions）、模型（Models）、视图（Views）等。

## 1. 结构解析
- **`ir.actions`**：表示 Odoo 的 "通用动作"（ir.actions），存储系统中的各种操作定义，如窗口动作、URL 动作、服务器动作等。
- **`ir.actions.act_window`**：表示 "窗口动作"（Window Actions），用于定义 Odoo 在用户界面中打开某个模型视图的行为。
- **`ir.actions.act_window.view`**：表示 "窗口动作的视图定义"，用于指定 `ir.actions.act_window` 打开时应使用哪些视图（列表、表单、看板等）。

## 2. `ir` 相关的其他常见模块
- **`ir.model`**：存储 Odoo 中所有模型的信息（类似 ORM 的元数据表）。
- **`ir.ui.view`**：存储 Odoo 的 XML 视图（表单、列表、搜索等）。
- **`ir.module.module`**：存储 Odoo 安装的模块信息。
- **`ir.cron`**：存储和管理 Odoo 的定时任务（cron jobs）。

## 3. 作用总结
在 Odoo 开发中，**`ir` 系列模块是系统管理和元数据存储的基础**，用于配置 Odoo 应用程序的核心功能。


# ir.model.access.csv 如何命名

以下是一个示例，适用于我们之前的 `test_model`：

```csv
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
access_test_model,access_test_model,model_test_model,base.group_user,1,0,0,0
```

# 字段说明

- **id**: 外部标识符。
- **name**: `ir.model.access` 的名称。
- **model_id/id**: 指定访问权限适用的模型。标准的引用方式是 `model_<model_name>`，其中 `<model_name>` 是模型的 `_name`，并将 `.` 替换为 `_`。虽然看起来有些繁琐，但这是标准做法。
- **group_id/id**: 指定访问权限适用的用户组。
- **perm_read, perm_write, perm_create, perm_unlink**: 分别表示读、写、创建和删除权限。


Actions can be triggered in three ways:

by clicking on menu items (linked to specific actions)

by clicking on buttons in views (if these are connected to actions)

as contextual actions on object



