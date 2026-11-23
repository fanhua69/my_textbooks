# 1.2.2 跨进程无锁环形缓冲区（SPSC / MPSC / MPMC Ring Buffer）

设计基于共享内存的零拷贝无锁队列，处理伪共享（False Sharing）与缓存行对齐。

---

## 导航

← 上一节：[1.2.1 共享内存中的 std::atomic 与内存序（Memory Order）](../01_共享内存中的_std_atomic_与内存序_memory_order/index.md)
↑ 返回上级：[1.2 跨进程同步原语与无锁内存模型](../index.md)
下一节：[1.2.3 跨进程阻塞等待与唤醒机制（futex / ulock / WaitOnAddress）](../03_跨进程阻塞等待与唤醒机制_futex_ulock_waitonaddress/index.md) →
