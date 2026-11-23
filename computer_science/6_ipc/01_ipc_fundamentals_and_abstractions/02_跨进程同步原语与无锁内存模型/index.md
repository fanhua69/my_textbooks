# 1.2 跨进程同步原语与无锁内存模型

解决共享内存与异步通知中的竞态问题，掌握跨进程锁、事件等待与共享内存中的原子操作。

## 本节目录

- [1.2.1 共享内存中的 std::atomic 与内存序（Memory Order）](01_共享内存中的_std_atomic_与内存序_memory_order/index.md)
- [1.2.2 跨进程无锁环形缓冲区（SPSC / MPSC / MPMC Ring Buffer）](02_跨进程无锁环形缓冲区_spsc_mpsc_mpmc_ring_buffer/index.md)
- [1.2.3 跨进程阻塞等待与唤醒机制（futex / ulock / WaitOnAddress）](03_跨进程阻塞等待与唤醒机制_futex_ulock_waitonaddress/index.md)

---

## 导航

← 上一节：[1.1 进程隔离与跨进程通信本质](../01_进程隔离与跨进程通信本质/index.md)
↑ 返回上级：[1 IPC 基础理论与核心抽象](../index.md)
下一节：[1.3 生命周期、身份认证与安全边界](../03_生命周期_身份认证与安全边界/index.md) →
