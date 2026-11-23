# 5.4.1 5.4.1_MPMC 的竞争结构与设计难点_mpmc_contention_and_challenges

分析 head/tail 竞争、槽位所有权、空满判断和节点回收。

---

## 导航

← 上一节：[5.3 5.3_MPSC 无锁队列_mpsc_lock_free_queue](../../5.3_MPSC 无锁队列_mpsc_lock_free_queue/index.md)
↑ 返回上级：[5.4 5.4_MPMC 无锁队列_mpmc_lock_free_queue](../index.md)
下一节：[5.4.2 5.4.2_Michael-Scott Lock-Free Queue_michael_scott_queue](../5.4.2_Michael-Scott Lock-Free Queue_michael_scott_queue/index.md) →
