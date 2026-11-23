# 5.4.1 MPMC 的竞争结构与设计难点  mpmc contention and challenges

分析 head/tail 竞争、槽位所有权、空满判断和节点回收。

---

## 导航

← 上一节：[5.3 MPSC 无锁队列  mpsc lock free queue](../../5.3_MPSC%20无锁队列_mpsc_lock_free_queue/index.md)
↑ 返回上级：[5.4 MPMC 无锁队列  mpmc lock free queue](../index.md)
下一节：[5.4.2 Michael-Scott Lock-Free Queue  michael scott queue](../5.4.2_Michael-Scott%20Lock-Free%20Queue_michael_scott_queue/index.md) →
