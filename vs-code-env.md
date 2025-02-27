
You: 

vs code 开发Odoo 环境配置, 详细到每一步

ChatGPT: 

在 VS Code 中配置 Odoo 开发环境涉及多个步骤，包括安装依赖、设置 Python 虚拟环境、下载 Odoo 源代码、配置数据库等。以下是详细步骤：


---

**1. 安装系统依赖** 
Odoo 依赖一些系统库，你需要先安装它们：
**Ubuntu/Debian** 

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv \
    git wget nodejs npm libpq-dev libxml2-dev libxslt1-dev \
    libldap2-dev libsasl2-dev libjpeg-dev libjpeg62-turbo-dev \
    zlib1g-dev libpq-dev libxslt-dev libevent-dev \
    libxrender1 xfonts-75dpi xfonts-base
```
**Windows**  
- 安装 [Python 3.x](https://www.python.org/downloads/)
 
- 安装 [Git](https://git-scm.com/downloads)
 
- 安装 [PostgreSQL](https://www.postgresql.org/download/)
 
- 安装 [Node.js]()


---

**2. 安装 VS Code 及必要插件**  
- 下载并安装 [VS Code](https://code.visualstudio.com/)
 
- 在 VS Code 中安装以下扩展： 
  - **Python** （Microsoft 提供）
 
  - **ODOO Snippets** （Odoo 开发支持）
 
  - **ODOO XML Snippets**
 
  - **ESLint** （JS 代码格式化）
 
  - **PostgreSQL** （数据库管理）


---

**3. 克隆 Odoo 源码** 

```bash
mkdir ~/odoo-dev && cd ~/odoo-dev
git clone https://github.com/odoo/odoo.git --branch 16.0 --single-branch
```
（`16.0` 可换成你需要的 Odoo 版本）

---

**4. 创建 Python 虚拟环境** 

```bash
cd ~/odoo-dev/odoo
python3 -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install --upgrade pip
```


---

**5. 安装 Odoo 依赖** 

```bash
pip install -r requirements.txt
```

如果是 Windows，可能需要手动安装某些库：


```bash
pip install psycopg2-binary lxml pillow
```


---

**6. 配置 PostgreSQL 数据库** **Ubuntu** 

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres psql
```

在 PostgreSQL 交互界面中执行：


```sql
CREATE USER odoo WITH CREATEDB PASSWORD 'odoo';
ALTER USER odoo WITH SUPERUSER;
```

然后退出：


```sql
\q
```
**Windows**  
- 打开 `pgAdmin`
 
- 创建一个新用户 `odoo`，密码 `odoo`
 
- 赋予 `SUPERUSER` 权限


---

**7. 创建 Odoo 配置文件** 创建 `odoo.conf` 文件：

```bash
mkdir ~/.odoo && nano ~/.odoo/odoo.conf
```

内容如下：


```ini
[options]
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
addons_path = ~/odoo-dev/odoo/addons,~/odoo-dev/custom_addons
xmlrpc_port = 8069
```


---

**8. 运行 Odoo** 
进入 Odoo 目录并启动：


```bash
cd ~/odoo-dev/odoo
python odoo-bin --config=~/.odoo/odoo.conf
```

如果要启用调试模式：


```bash
python odoo-bin --config=~/.odoo/odoo.conf --dev=all
```


---

**9. 在 VS Code 配置调试** 在 VS Code 中，打开 `.vscode/launch.json` 并添加：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Odoo Debug",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/odoo-bin",
            "args": [
                "--config=${workspaceFolder}/.odoo/odoo.conf",
                "--dev=all"
            ],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```
然后点击 **Run and Debug**  开始调试。

---

**10. 访问 Odoo** 
打开浏览器，访问：


```arduino
http://localhost:8069
```
首次运行需要创建数据库，输入 `odoo` 用户和密码 `admin` 进行操作。

---

**11. 创建自定义模块** 在 `~/odoo-dev/custom_addons/` 目录中创建一个新模块：

```bash
mkdir -p ~/odoo-dev/custom_addons/my_module
cd ~/odoo-dev/custom_addons/my_module
```

创建必要的文件：


```bash
touch __init__.py __manifest__.py models.py
```
示例 `__manifest__.py`：

```python
{
    'name': 'My Custom Module',
    'version': '16.0.1.0.0',
    'depends': ['base'],
    'data': [],
    'installable': True,
    'application': True,
}
```

然后在 VS Code 开发即可！


---

**到此，你的 Odoo 开发环境已配置完成 🎉**
