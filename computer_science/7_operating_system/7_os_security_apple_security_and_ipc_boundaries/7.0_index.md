# 7 操作系统安全模型、苹果安全机制与 IPC 通信边界

**介绍**: 系统讲解权限与访问控制模型、代码签名与沙盒、IPC 攻击面防护，深入剖析苹果生态下的 TCC / PPPC、Security Framework、Authorization Services 与特权/非特权多进程 XPC 通信边界设计，并对比 Linux 与 Windows 安全机制。

## 目录

- [7.1 操作系统安全基础与 IPC 信任边界](7.1_操作系统安全基础与_ipc_信任边界/index.md)
- [7.2 苹果平台安全机制：TCC / PPPC、Security Framework 与 Authorization Services](7.2_苹果平台安全机制_tcc_pppc_security_framework_与_authorization_services/index.md)
- [7.3 macOS 特权与非特权多进程 XPC 通信边界设计](7.3_macos_特权与非特权多进程_xpc_通信边界设计/index.md)
- [7.4 Linux 与 Windows 安全与 IPC 权限边界对比](7.4_linux_与_windows_安全与_ipc_权限边界对比/index.md)

## 导航

← 上一节：[6 任务调度、CPU Binding 与尾延迟（P99 / P99.9）治理](../6_task_scheduling_cpu_binding_and_tail_latency/index.md)
↑ 返回上级：[Operating Systems Engineering: Low-Latency & Systems Architecture (Linux, macOS & Windows)](../index.md)
下一节：[8 常用命令行工具、内核性能剖析与低延迟实战](../8_cli_tools_profiling_and_low_latency_practice/index.md) →
