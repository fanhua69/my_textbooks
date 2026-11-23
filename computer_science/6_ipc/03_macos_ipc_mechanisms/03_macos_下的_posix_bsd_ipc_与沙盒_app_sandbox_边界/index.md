# 3.3 macOS 下的 POSIX / BSD IPC 与沙盒（App Sandbox）边界

对比 macOS 与 Linux 在 POSIX IPC 上的细微差异及 App Sandbox 安全约束。

## 本节目录

- [3.3.1 macOS 共享内存（shm_open / mach_vm_remap）与 xpc  shmem](01_macos_共享内存_shm_open_mach_vm_remap_与_xpc_shmem/index.md)
- [3.3.2 UNIX Domain Socket、kqueue 与 macOS POSIX 信号量限制](02_unix_domain_socket_kqueue_与_macos_posix_信号量限制/index.md)
- [3.3.3 App Group 容器、NSDistributedNotificationCenter 与 System Extension 通信](03_app_group_容器_nsdistributednotificationcenter_与_system_extension_通信/index.md)

---

## 导航

← 上一节：[3.2 XPC 框架：macOS 现代 IPC 核心](../02_xpc_框架_macos_现代_ipc_核心/index.md)
↑ 返回上级：[3 macOS（XNU / Darwin）平台 IPC 机制深度剖析](../index.md)
下一节：[4 Windows 平台 IPC 机制深度剖析](../../04_windows_ipc_mechanisms/index.md) →
