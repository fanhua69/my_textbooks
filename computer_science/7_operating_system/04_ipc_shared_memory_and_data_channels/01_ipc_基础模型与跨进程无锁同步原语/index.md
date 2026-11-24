# 4.1 IPC 基础模型与跨进程无锁同步原语

从地址空间隔离与缓存一致性出发，掌握共享内存原子同步、无锁环形队列与用户态等待唤醒原语。

## 本节目录

- [4.1.1 IPC 通信范式对比：消息传递、字节流、共享内存、RPC 与事件通知](01_ipc_通信范式对比与适用边界/index.md)
- [4.1.2 共享内存中的 std::atomic、内存序与无锁环形缓冲区（SPSC / MPMC）](02_共享内存原子同步与无锁环形缓冲区/index.md)
- [4.1.3 跨进程阻塞等待与唤醒原语：futex / ulock / WaitOnAddress](03_跨进程阻塞等待与唤醒原语对比/index.md)

---

## 导航

← 上一节：[3 虚拟内存、TLB、Cache Line、CPU、NUMA、DMA 与硬件内存体系](../../03_virtual_memory_tlb_cache_line_cpu_numa_and_dma/index.md)
↑ 返回上级：[4 进程间通信（IPC）、共享内存与高速数据通道](../index.md)
下一节：[4.2 Linux、macOS 与 Windows 核心 IPC 机制详解](../02_linux_macos_与_windows_核心_ipc_机制详解/index.md) →
