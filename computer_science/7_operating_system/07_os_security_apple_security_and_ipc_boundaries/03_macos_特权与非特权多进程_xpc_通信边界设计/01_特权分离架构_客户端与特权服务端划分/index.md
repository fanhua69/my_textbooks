# 01 特权分离架构：非特权客户端与特权服务端划分

**介绍**: 明确特权边界与责任划分，避免非特权进程直接触碰高危系统状态，并处理多用户会话与守护进程生命周期。

## 目录

- [01 非特权 App / LaunchAgent / CLI 与特权 root LaunchDaemon / System Extension 分工](01_客户端与特权服务端职责划分/index.md)
- [02 多用户会话与守护进程按需拉起/崩溃重连设计](02_多用户会话与按需拉起_崩溃重连设计/index.md)

## 导航

← 上一节：[7.2 苹果平台安全机制：TCC / PPPC、Security Framework 与 Authorization Services](../../02_苹果平台安全机制_tcc_pppc_security_framework_与_authorization_services/index.md)
↑ 返回上级：[7.3 macOS 特权与非特权多进程 XPC 通信边界设计](../index.md)
下一节：[7.3.2 XPC 服务端调用方校验（Audit Token / Signing Requirement）与严格参数校验](../02_xpc_服务端身份校验与严格参数校验/index.md) →
