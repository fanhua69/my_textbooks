# 7.3.1.2 多用户会话与守护进程按需拉起/崩溃重连设计

**介绍**: 处理连接中断与作废事件、多会话并发请求以及守护进程重启后的状态同步。

---

## 导航

← 上一节：[7.3.1.1 非特权 App / LaunchAgent / CLI 与特权 root LaunchDaemon / System Extension 分工](../7.3.1.1_客户端与特权服务端职责划分/index.md)
↑ 返回上级：[7.3.1 特权分离架构：非特权客户端与特权服务端划分](../index.md)
下一节：[7.3.2 XPC 服务端调用方校验（Audit Token / Signing Requirement）与严格参数校验](../../7.3.2_xpc_服务端身份校验与严格参数校验/index.md) →
