# 02 Linux、macOS 与 Windows 核心 IPC 机制详解

**介绍**: 逐一拆解三大操作系统的主力 IPC 通道、描述符/句柄传递能力及平台特有行为。

## 目录

- [01 Linux IPC：UNIX Domain Socket（SCM RIGHTS）、memfd + File Sealing、eventfd 与管道](01_linux_ipc_af_unix_memfd_eventfd_与管道/index.md)
- [02 macOS IPC：Mach Port / mach msg、XPC（libxpc / NSXPCConnection）、xpc shmem 与 POSIX IPC](02_macos_ipc_mach_port_xpc_与_posix_差异/index.md)
- [03 Windows IPC：Named Pipes（Overlapped / IOCP）、File Mapping、WaitOnAddress、AF UNIX 与 ALPC/RPC](03_windows_ipc_named_pipes_file_mapping_alpc_与_rpc/index.md)

## 导航

← 上一节：[4.1 IPC 基础模型与跨进程无锁同步原语](../01_ipc_基础模型与跨进程无锁同步原语/index.md)
↑ 返回上级：[4 进程间通信（IPC）、共享内存与高速数据通道](../index.md)
下一节：[4.3 低延迟 IPC 架构：控制面 + 数据面分离与崩溃恢复](../03_低延迟_ipc_架构_控制面_数据面与崩溃恢复/index.md) →
