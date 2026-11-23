# 5.3 5.3_MPSC 无锁队列_mpsc_lock_free_queue

研究多个生产者并发提交、单消费者串行处理的结构。

## 本节目录

- [5.3.1 5.3.1_MPSC 的并发约束与典型场景_mpsc_constraints_and_use_cases](5.3.1_MPSC 的并发约束与典型场景_mpsc_constraints_and_use_cases/index.md)
- [5.3.2 5.3.2_基于 CAS 的 MPSC 入队_mpsc_cas_enqueue](5.3.2_基于 CAS 的 MPSC 入队_mpsc_cas_enqueue/index.md)
- [5.3.3 5.3.3_单消费者出队路径_mpsc_single_consumer_dequeue](5.3.3_单消费者出队路径_mpsc_single_consumer_dequeue/index.md)
- [5.3.4 5.3.4_Intrusive MPSC Queue_intrusive_mpsc_queue](5.3.4_Intrusive MPSC Queue_intrusive_mpsc_queue/index.md)
- [5.3.5 5.3.5_MPSC 的空队列与链表断链窗口_mpsc_empty_and_linking_window](5.3.5_MPSC 的空队列与链表断链窗口_mpsc_empty_and_linking_window/index.md)
- [5.3.6 5.3.6_MPSC 有界队列与序列号方案_bounded_mpsc_sequence_queue](5.3.6_MPSC 有界队列与序列号方案_bounded_mpsc_sequence_queue/index.md)

---

## 导航

← 上一节：[5.2 5.2_SPSC 无锁队列_spsc_lock_free_queue](../5.2_SPSC 无锁队列_spsc_lock_free_queue/index.md)
↑ 返回上级：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../index.md)
下一节：[5.4 5.4_MPMC 无锁队列_mpmc_lock_free_queue](../5.4_MPMC 无锁队列_mpmc_lock_free_queue/index.md) →
