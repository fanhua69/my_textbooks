# 3.3.1 macOS 共享内存（shm_open / mach_vm_remap）与 xpc  shmem

**介绍**: 解决沙盒环境下 POSIX 共享内存命名受限问题，结合 XPC 传递共享内存区域实现高速数据面。

---

## 导航

← 上一节：[3.2 XPC 框架：macOS 现代 IPC 核心](../../3.2_xpc_框架_macos_现代_ipc_核心/index.md)
↑ 返回上级：[3.3 macOS 下的 POSIX / BSD IPC 与沙盒（App Sandbox）边界](../index.md)
下一节：[3.3.2 UNIX Domain Socket、kqueue 与 macOS POSIX 信号量限制](../3.3.2_unix_domain_socket_kqueue_与_macos_posix_信号量限制/index.md) →
