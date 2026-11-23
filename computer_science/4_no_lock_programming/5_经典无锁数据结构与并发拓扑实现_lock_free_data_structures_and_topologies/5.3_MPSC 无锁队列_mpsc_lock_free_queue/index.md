# 5.3 MPSC 无锁队列  mpsc lock free queue

研究多个生产者并发提交、单消费者串行处理的结构。

## 本节目录

- [5.3.1 MPSC 的并发约束与典型场景  mpsc constraints and use cases](5.3.1_MPSC%20的并发约束与典型场景_mpsc_constraints_and_use_cases/index.md)
- [5.3.2 基于 CAS 的 MPSC 入队  mpsc cas enqueue](5.3.2_基于%20CAS%20的%20MPSC%20入队_mpsc_cas_enqueue/index.md)
- [5.3.3 单消费者出队路径  mpsc single consumer dequeue](5.3.3_单消费者出队路径_mpsc_single_consumer_dequeue/index.md)
- [5.3.4 Intrusive MPSC Queue  intrusive mpsc queue](5.3.4_Intrusive%20MPSC%20Queue_intrusive_mpsc_queue/index.md)
- [5.3.5 MPSC 的空队列与链表断链窗口  mpsc empty and linking window](5.3.5_MPSC%20的空队列与链表断链窗口_mpsc_empty_and_linking_window/index.md)
- [5.3.6 MPSC 有界队列与序列号方案  bounded mpsc sequence queue](5.3.6_MPSC%20有界队列与序列号方案_bounded_mpsc_sequence_queue/index.md)

---

## 导航

← 上一节：[5.2 SPSC 无锁队列  spsc lock free queue](../5.2_SPSC%20无锁队列_spsc_lock_free_queue/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.4 MPMC 无锁队列  mpmc lock free queue](../5.4_MPMC%20无锁队列_mpmc_lock_free_queue/index.md) →
