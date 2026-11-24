# 18.2 硬件亲和性 (Mechanical Sympathy)、内存模型与无锁并发

**介绍**: 顺应现代多核 CPU 缓存架构与内存子系统物理特性设计高性能软件。

## 目录

- [18.2.1 CPU 缓存层次、缓存行与伪共享消除](18.2.1_CPU缓存层次_缓存行与伪共享消除/index.md)
- [18.2.2 内存屏障、内存序与无锁并发架构](18.2.2_内存屏障_内存序与无锁并发架构/index.md)
- [18.2.3 零拷贝 (Zero-Copy) 与对象池化内存治理](18.2.3_零拷贝与对象池化内存治理_Zero-Copy/index.md)
- [18.2.4 无锁数据结构：无锁栈、无锁队列与 SPSC / MPSC / SPMC / MPMC](18.2.4_无锁数据结构_无锁栈_无锁队列与_SPSC_MPSC_SPMC_MPMC/index.md)
- [18.2.5 ABA 问题、风险指针 (Hazard Pointer) 与 RCU 内存回收](18.2.5_ABA_问题_风险指针_Hazard_Pointer_与_RCU_内存回收/index.md)
- [18.2.6 NUMA 架构与 CPU 亲和性 (CPU Affinity)](18.2.6_NUMA_架构与_CPU_亲和性_CPU_Affinity/index.md)
- [18.2.7 内存分配器与分配策略：tcmalloc、jemalloc 与 Arena](18.2.7_内存分配器与分配策略_tcmalloc_jemalloc_与_Arena/index.md)

## 导航

← 上一节：[18.1 并发基础与同步模式](../18.1_并发基础与同步模式/index.md)
↑ 返回上级：[18 并发、系统性能与底层架构工程](../index.md)
下一节：[18.3 高并发网络 I/O 模型与异步架构](../18.3_高并发网络IO模型与异步架构/index.md) →
