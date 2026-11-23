# 5.4 5.4_MPMC 无锁队列_mpmc_lock_free_queue

研究多生产者、多消费者同时入队和出队时的协调机制。

## 本节目录

- [5.4.1 5.4.1_MPMC 的竞争结构与设计难点_mpmc_contention_and_challenges](5.4.1_MPMC 的竞争结构与设计难点_mpmc_contention_and_challenges/index.md)
- [5.4.2 5.4.2_Michael-Scott Lock-Free Queue_michael_scott_queue](5.4.2_Michael-Scott Lock-Free Queue_michael_scott_queue/index.md)
- [5.4.3 5.4.3_Bounded MPMC Array Queue_bounded_mpmc_array_queue](5.4.3_Bounded MPMC Array Queue_bounded_mpmc_array_queue/index.md)
- [5.4.4 5.4.4_Per-Slot Sequence Number_per_slot_sequence_number](5.4.4_Per-Slot Sequence Number_per_slot_sequence_number/index.md)
- [5.4.5 5.4.5_MPMC 的线性化点与正确性_mpmc_linearization_and_correctness](5.4.5_MPMC 的线性化点与正确性_mpmc_linearization_and_correctness/index.md)
- [5.4.6 5.4.6_MPMC 的扩展性与热点分析_mpmc_scalability_and_contention](5.4.6_MPMC 的扩展性与热点分析_mpmc_scalability_and_contention/index.md)

---

## 导航

← 上一节：[5.3 5.3_MPSC 无锁队列_mpsc_lock_free_queue](../5.3_MPSC 无锁队列_mpsc_lock_free_queue/index.md)
↑ 返回上级：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../index.md)
下一节：[5.5 5.5_SPMC 与广播/扇出结构_spmc_and_broadcast_queues](../5.5_SPMC 与广播_扇出结构_spmc_and_broadcast_queues/index.md) →
