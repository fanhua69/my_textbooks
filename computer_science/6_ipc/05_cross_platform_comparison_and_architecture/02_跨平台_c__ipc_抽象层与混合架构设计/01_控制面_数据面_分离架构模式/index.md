# 01 “控制面 + 数据面”分离架构模式

**介绍**: 控制面（XPC / AF_UNIX / Named Pipe）负责握手与认证，数据面（Shm + 无锁队列）负责零拷贝流转。

---

## 导航

← 上一节：[5.1 Linux、macOS 与 Windows IPC 机制全景对比](../../01_linux_macos_与_windows_ipc_机制全景对比/index.md)
↑ 返回上级：[5.2 跨平台 C++ IPC 抽象层与混合架构设计](../index.md)
下一节：[5.2.2 统一 C++20 抽象接口设计（Channel / SharedRegion / Notifier）](../02_统一_c_20_抽象接口设计_channel_sharedregion_notifier/index.md) →
