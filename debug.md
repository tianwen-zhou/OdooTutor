# 插件模块目录和Odoo在不同的目录之下，如何避免copy插件模块目录到Odoo目录开发调试问题？

# 在 VS Code 中让 `custom_addons` 目录成为 Workspace

## 步骤

1. **打开 `custom_addons` 目录**
   - 在 VS Code 中，选择 **File -> Open Folder**
   - 选择 `custom_addons` 目录并打开

2. **在 VS Code 里添加 Odoo 目录作为 Workspace**
   - 依次点击 **File -> Add Folder to Workspace**
   - 选择 `/home/user/odoo` 目录

3. **最终效果**
   - `custom_addons` 作为主开发目录
   - `odoo` 目录也在 VS Code 中，可用于阅读和修改 Odoo 代码
   - 这样既可以编辑 Odoo 代码，又能开发自定义模块

4. **可选：保存 Workspace**
   - 依次点击 **File -> Save Workspace As...**
   - 选择保存路径，方便下次直接打开

这样你就可以高效地开发和调试 Odoo 自定义模块了！🚀




实用的 VS Code 快捷键
---------------

*   **F9**: 设置/取消断点
*   **F5**: 启动调试
*   **F10**: 单步执行（不进入函数）
*   **F11**: 单步进入（进入函数）
*   **Shift+F11**: 单步跳出（退出当前函数）
*   **Ctrl+Shift+F5**: 重启调试会话
*   **Shift+F5**: 停止调试
