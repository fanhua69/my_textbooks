# 3.2 XPC 框架：macOS 现代 IPC 核心

全面掌握苹果官方推荐的 XPC C API 与 NSXPCConnection 架构。

## 本节目录

- [3.2.1 底层 C API（libxpc / xpc connection t）与序列化类型系统](01_底层_c_api_libxpc_xpc_connection_t_与序列化类型系统/index.md)
- [3.2.2 NSXPCConnection、NSXPCInterface 与远程对象代理](02_nsxpcconnection_nsxpcinterface_与远程对象代理/index.md)
- [3.2.3 按需启动（On-Demand）、连接中断（Interruption）与作废（Invalidation）](03_按需启动_on_demand_连接中断_interruption_与作废_invalidation/index.md)
- [3.2.4 Audit Token 校验与代码签名（Code Signing Requirement）安全加固](04_audit_token_校验与代码签名_code_signing_requirement_安全加固/index.md)

---

## 导航

← 上一节：[3.1 XNU 混合内核与 Mach Ports 底层原语](../01_xnu_混合内核与_mach_ports_底层原语/index.md)
↑ 返回上级：[3 macOS（XNU / Darwin）平台 IPC 机制深度剖析](../index.md)
下一节：[3.3 macOS 下的 POSIX / BSD IPC 与沙盒（App Sandbox）边界](../03_macos_下的_posix_bsd_ipc_与沙盒_app_sandbox_边界/index.md) →
