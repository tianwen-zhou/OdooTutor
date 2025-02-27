VS Code配置Odoo开发环境
-----------------

### 1\. 安装VS Code

首先确保您已安装最新版本的Visual Studio Code。

### 2\. 安装必要的VS Code扩展

这些扩展将使您的Odoo开发更高效：

*   Python扩展（Microsoft官方）- 提供Python语言支持
*   Odoo Snippets - 提供Odoo代码片段
*   XML Tools - 用于XML文件格式化和验证
*   Pylint - Python代码质量检查
*   GitLens - 更好的Git集成（如果您使用Git）

### 3\. 配置Python环境

*   安装Python（建议3.7+，与您的Odoo版本兼容）
*   创建虚拟环境：
    
    ```bash
    python -m venv odoo-venv
    ```
    
*   在VS Code中选择此虚拟环境（通过命令面板：Python: Select Interpreter）

### 4\. 克隆或下载Odoo源码

您需要有Odoo源码以便VS Code可以提供正确的自动完成和导航：

```bash
git clone https://github.com/odoo/odoo.git
```

### 5\. 配置VS Code工作区设置

创建`.vscode/settings.json`文件在您的项目根目录：

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--load-plugins=pylint_odoo",
        "--disable=all",
        "--enable=odoolint"
    ],
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}/odoo",
        "${workspaceFolder}/addons"
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}/odoo",
        "${workspaceFolder}/addons"
    ],
    "files.exclude": {
        "**/*.pyc": true,
        "**/__pycache__": true
    }
}
```

### 6\. 安装Odoo开发所需的Python包

在您的虚拟环境中安装所需的依赖项：

```bash
pip install -r odoo/requirements.txt
pip install pylint-odoo
```

### 7\. 添加调试配置

创建`.vscode/launch.json`文件以便调试Odoo：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Odoo",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/odoo/odoo-bin",
            "args": [
                "--config=${workspaceFolder}/odoo.conf",
                "--dev=all"
            ],
            "console": "integratedTerminal"
        }
    ]
}
```

### 8\. 创建Odoo配置文件

创建`odoo.conf`文件在您的项目根目录：

```
[options]
addons_path = ./odoo/addons,./custom_addons
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
http_port = 8069
```

现在您的VS Code已经配置好可以用于Odoo开发。您可以通过按F5开始调试模式，这将启动Odoo服务器，并可以设置断点进行调试。

您需要根据自己的具体情况调整路径和配置选项。这个设置适合大多数Odoo开发场景，但可能需要根据您的特定项目进行微调。

