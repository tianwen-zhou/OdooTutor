# 详解 Odoo pos 离线模式



**Odoo POS 离线模式详解** Odoo **POS（Point of Sale）**  具有 **离线模式（Offline Mode）** ，允许 POS 终端在 **网络断开**  的情况下继续运行，并在恢复连接后自动同步数据。 **离线模式的核心机制** ： 
1. **使用浏览器缓存和 IndexedDB**  存储销售数据、产品信息等。
 
2. **Service Worker**  拦截请求，确保离线时 POS 界面可用。
 
3. **本地存储销售记录** ，网络恢复后同步到 Odoo 服务器。


---

**1. Odoo POS 离线模式的关键组件** **🔹 1.1. IndexedDB：本地存储** Odoo POS 主要使用 **IndexedDB**  存储： 
- **订单数据**
 
- **产品信息**
 
- **客户信息**
 
- **付款记录**
 
- **会话数据**
📌 **数据存储示例** 

```js
var request = indexedDB.open("odoo_pos", 1);
request.onsuccess = function(event) {
    var db = event.target.result;
    var transaction = db.transaction(["orders"], "readwrite");
    var store = transaction.objectStore("orders");
    
    var orderData = { id: "order_123", total: 100, status: "pending" };
    store.put(orderData);
};
```


---

**🔹 1.2. Service Worker：缓存 POS 资源** Odoo POS 使用 **Service Worker**  缓存静态资源，例如：
- HTML、CSS、JS 文件

- 产品图片

- POS 终端界面
📌 **Service Worker 示例** 

```js
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('pos-cache-v1').then(cache => {
            return cache.addAll([
                '/',
                '/pos/index.html',
                '/pos/static/js/main.js',
                '/pos/static/css/style.css',
                '/pos/static/images/logo.png'
            ]);
        })
    );
});
```
📌 **作用**  
- 在 **离线模式**  下提供 POS UI 访问
 
- **拦截请求** ，如果网络不可用，则使用缓存数据


---

**🔹 1.3. Odoo POS WebSocket & API**  
- **在线模式** ：使用 WebSocket 连接 Odoo 服务器，实时获取数据。
 
- **离线模式** ：
  - 断开 WebSocket 连接
 
  - 订单数据暂存于 **IndexedDB**
 
  - 网络恢复后，使用 **Odoo JSON-RPC API**  同步数据
📌 **数据同步 API** 

```json
POST /pos_order/sync
{
  "orders": [
    {
      "id": "order_123",
      "total": 100,
      "lines": [
        {"product_id": 1, "qty": 2, "price": 50}
      ]
    }
  ]
}
```


---

**2. Odoo POS 离线模式的工作流程** **🛠 2.1. 离线状态（No Internet）**  
1. **POS 仍然可以使用** （因为 UI 资源已缓存）。
 
2. **所有交易（订单、付款等）存储在 IndexedDB** 。
 
3. **Service Worker 缓存静态文件** ，保证页面可访问。
**🔄 2.2. 重新联网（Internet Restored）**  
1. **检测网络状态** ，自动尝试重新连接服务器。
 
2. **POS 会话恢复** （与 Odoo 服务器同步）。
 
3. **未同步的订单自动上传**  到服务器：
  - 读取 IndexedDB 的订单数据。

  - 通过 Odoo API 发送数据（JSON-RPC）。

  - 服务器确认后删除本地缓存。
📌 **网络恢复后同步代码** 

```js
if (navigator.onLine) {
    syncOrdersWithServer();
}

function syncOrdersWithServer() {
    var request = indexedDB.open("odoo_pos");
    request.onsuccess = function(event) {
        var db = event.target.result;
        var transaction = db.transaction(["orders"], "readwrite");
        var store = transaction.objectStore("orders");

        store.getAll().onsuccess = function(event) {
            let orders = event.target.result;
            if (orders.length > 0) {
                fetch('/pos_order/sync', {
                    method: 'POST',
                    body: JSON.stringify({ orders }),
                    headers: { 'Content-Type': 'application/json' }
                }).then(response => {
                    if (response.ok) {
                        // 清除已同步订单
                        store.clear();
                    }
                });
            }
        };
    };
}
```


---

**3. 配置 Odoo POS 离线模式** **✅ 3.1. 确保启用离线模式**  
- **进入 Odoo 后台**
 
- **导航到**  `Point of Sale` > `Settings`
 
- **勾选**  ✅ `Allow Offline Mode`
📌 **确保缓存资源生效** 

```bash
sudo systemctl restart odoo
```


---

**4. Odoo POS 离线模式的限制** | 限制 | 说明 | 
| --- | --- | 
| 🔴 数据同步有延迟 | 离线订单不会立即出现在 Odoo 后台，必须等待网络恢复。 | 
| 🔴 库存数据可能不准确 | 离线模式下库存不会实时更新，可能导致超卖。 | 
| 🔴 仅支持基本销售功能 | 复杂操作（如退款、促销规则）可能无法在离线模式下完成。 | 
| 🔴 浏览器兼容性 | IndexedDB 和 Service Worker 可能在 Safari 早期版本 存在兼容性问题。 | 


---

**5. 如何增强 Odoo POS 离线模式** | 方法 | 解决方案 | 
| --- | --- | 
| ✅ 使用 PWA（渐进式 Web 应用） | 让 POS 可以安装在设备上，提供更好的离线支持。 | 
| ✅ 手动触发同步 | 添加“手动同步”按钮，让店员可以在网络恢复时立即上传数据。 | 
| ✅ 缓存更多数据 | 预加载商品数据、客户信息，提高离线可用性。 | 
| ✅ 多终端数据合并 | 设计更智能的订单合并逻辑，避免冲突。 | 
📌 **示例：手动触发同步** 

```html
<button onclick="syncOrdersWithServer()">同步订单</button>
```


---

**6. 总结** ✅ **Odoo POS 离线模式**  允许用户在断网状态下继续销售，并在网络恢复后自动同步数据。
✅ **关键技术** ： 
- **IndexedDB**  存储订单数据
 
- **Service Worker**  缓存 UI
 
- **Odoo API**  进行数据同步
⚠️ **注意事项**  
- **库存数据**  在离线模式下不会实时更新
 
- **复杂操作（退款、促销）**  可能受限
 
- **多终端同步**  需要额外优化
📌 如果你的 POS 需要 **更强的离线支持** ，可以考虑 **Odoo Enterprise 版本** ，或使用 **本地服务器**  方案！ 🚀
