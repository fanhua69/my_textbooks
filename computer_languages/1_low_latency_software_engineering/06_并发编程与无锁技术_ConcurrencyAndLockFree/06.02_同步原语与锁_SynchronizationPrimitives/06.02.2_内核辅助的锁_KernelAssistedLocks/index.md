# 6.2.2 内核辅助的锁

无争用走用户态而争用时进入内核。

## 本节目录

- [6.2.2.1 mutex、futex 与自适应互斥](06.02.2.1_mutex_futex_与自适应互斥_MutexFutexAdaptive/index.md)
- [6.2.2.2 读写锁、seqlock 与 RCU 读侧](06.02.2.2_读写锁_seqlock_与_RCU_读侧_RWLockSeqlockRCU/index.md)
- [6.2.2.3 条件变量、信号量与 eventfd](06.02.2.3_条件变量_信号量与_eventfd_CondVarSemaphoreEventfd/index.md)

---

## 导航

← 上一节：[6.2.1 原子读改写与自旋锁](../06.02.1_原子读改写与自旋锁_AtomicRMWSpinlocks/index.md)
↑ 返回上级：[6.2 同步原语与锁](../index.md)
下一节：[6.2.3 事务内存与锁省略](../06.02.3_事务内存与锁省略_TransactionalMemory/index.md) →
