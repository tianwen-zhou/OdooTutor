SDK版本兼容问题

# Android 12+ 广播注册问题解决方案  

您看到的错误表明 **ACLAS 秤 SDK** 内部代码使用了不兼容 **Android 12+** 的广播注册方式。由于这个错误发生在 SDK 的封闭代码中 (`com.example.io.USBPort.ALLATORIxDEMO`)，我们无法直接修改它。  

## **解决方案：降低目标 SDK 版本**  
在 `app/build.gradle` 文件中修改 `targetSdkVersion`：  

```gradle
android {
    defaultConfig {
        // 其他设置保持不变...
        targetSdkVersion 30  // 降为 Android 11
    }
}

为什么这样能解决问题?
在 Android 12 (API 31) 及以上版本，广播接收器必须指定 RECEIVER_EXPORTED 或 RECEIVER_NOT_EXPORTED 标志。

ACLAS 秤 SDK 在内部使用了旧的注册方式：

kotlin
Copy
Edit
context.registerReceiver(receiver, filter)
降低 targetSdkVersion 让应用在兼容模式下运行，无需这些新标志。

其他可能解决方案
使用反射修改 SDK 行为：技术上可行，但不推荐，容易引入新问题。

自行实现 USB 通信层：不依赖 SDK 的广播接收器，但工作量大。

联系 ACLAS 获取更新的 SDK：长期解决方案，如果 ACLAS 提供了兼容 Android 12+ 的新 SDK，最好使用官方更新。

现有 ScaleManager 类
我之前提供的 ScaleManager.kt 已经实现了：
✅ 更好的线程安全性
✅ 异常处理
✅ 防重复连接
✅ 资源安全释放

但无法解决 SDK 内部代码的问题，所以必须通过降低目标 SDK 版本来解决。

实施步骤
修改 app/build.gradle 中的 targetSdkVersion。

使用我之前提供的 ScaleManager.kt 替换原来的类。

运行：

sh
Copy
Edit
./gradlew clean
重新构建和安装应用。

完成这些步骤后，应用应该能够正常连接和使用 ACLAS 电子秤了。 🎯

Copy
Edit

这个 Markdown 版本可以直接用于文档、GitHub README 或博客文章。你是否需要进一步优化？ 
