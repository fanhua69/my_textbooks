# 1.2.1 共享内存中的 std::atomic 与内存序（Memory Order）

**介绍**: 理解 lock-free 原子对象在跨进程映射内存中的合法性要求、缓存一致性与 acquire-release 语义。

---

## 导航

← 上一节：[1.1 进程隔离与跨进程通信本质](../../1.1_进程隔离与跨进程通信本质/index.md)
↑ 返回上级：[1.2 跨进程同步原语与无锁内存模型](../index.md)
下一节：[1.2.2 跨进程无锁环形缓冲区（SPSC / MPSC / MPMC Ring Buffer）](../1.2.2_跨进程无锁环形缓冲区_spsc_mpsc_mpmc_ring_buffer/index.md) →
