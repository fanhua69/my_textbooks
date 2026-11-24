# 01 IPC 通信范式对比：消息传递、字节流、共享内存、RPC 与事件通知

**介绍**: 分析不同 IPC 机制的拷贝次数、序列化成本、消息边界保证与延迟特性。

---

## 导航

← 上一节：[3 虚拟内存、TLB、Cache Line、CPU、NUMA、DMA 与硬件内存体系](../../../03_virtual_memory_tlb_cache_line_cpu_numa_and_dma/index.md)
↑ 返回上级：[4.1 IPC 基础模型与跨进程无锁同步原语](../index.md)
下一节：[4.1.2 共享内存中的 std::atomic、内存序与无锁环形缓冲区（SPSC / MPMC）](../02_共享内存原子同步与无锁环形缓冲区/index.md) →
