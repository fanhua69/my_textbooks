# 4.3 低延迟 IPC 架构：控制面 + 数据面分离与崩溃恢复

将安全/生命周期管理与高频零拷贝数据流解耦，构建高可用、抗崩溃的跨进程数据通路。

## 本节目录

- [4.3.1 控制面（XPC / AF UNIX / Named Pipe）握手与数据面（共享内存）建链](01_控制面握手与共享内存数据面建链/index.md)
- [4.3.2 对端异常退出、僵尸状态检测、重连与共享内存不变量恢复](02_对端崩溃检测_重连与共享内存状态恢复/index.md)

---

## 导航

← 上一节：[4.2 Linux、macOS 与 Windows 核心 IPC 机制详解](../02_linux_macos_与_windows_核心_ipc_机制详解/index.md)
↑ 返回上级：[4 进程间通信（IPC）、共享内存与高速数据通道](../index.md)
下一节：[5 文件系统、存储 I/O 栈与持久化性能](../../05_file_systems_storage_io_and_persistence/index.md) →
