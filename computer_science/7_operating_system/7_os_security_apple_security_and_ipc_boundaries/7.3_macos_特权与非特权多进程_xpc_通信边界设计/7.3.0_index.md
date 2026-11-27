# 7.3 macOS 特权与非特权多进程 XPC 通信边界设计

**介绍**: 围绕特权守护进程/扩展与非特权 App/Agent/CLI 的多进程架构，设计可审计、抗攻击、低开销的 XPC 边界。

## 目录

- [7.3.1 特权分离架构：非特权客户端与特权服务端划分](7.3.1_特权分离架构_客户端与特权服务端划分/index.md)
- [7.3.2 XPC 服务端调用方校验（Audit Token / Signing Requirement）与严格参数校验](7.3.2_xpc_服务端身份校验与严格参数校验/index.md)
- [7.3.3 XPC 控制面与高速数据面解耦及崩溃隔离](7.3.3_xpc_控制面与高速数据面解耦及崩溃隔离/index.md)

## 导航

← 上一节：[7.2 苹果平台安全机制：TCC / PPPC、Security Framework 与 Authorization Services](../7.2_苹果平台安全机制_tcc_pppc_security_framework_与_authorization_services/index.md)
↑ 返回上级：[7 操作系统安全模型、苹果安全机制与 IPC 通信边界](../index.md)
下一节：[7.4 Linux 与 Windows 安全与 IPC 权限边界对比](../7.4_linux_与_windows_安全与_ipc_权限边界对比/index.md) →
