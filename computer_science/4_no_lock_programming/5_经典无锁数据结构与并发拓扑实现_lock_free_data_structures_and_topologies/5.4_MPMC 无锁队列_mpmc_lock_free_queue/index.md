# 5.4 MPMC 无锁队列  mpmc lock free queue

**介绍**: 研究多生产者、多消费者同时入队和出队时的协调机制。

## 目录

- [5.4.1 MPMC 的竞争结构与设计难点  mpmc contention and challenges](5.4.1_MPMC%20%E7%9A%84%E7%AB%9E%E4%BA%89%E7%BB%93%E6%9E%84%E4%B8%8E%E8%AE%BE%E8%AE%A1%E9%9A%BE%E7%82%B9_mpmc_contention_and_challenges/index.md)
- [5.4.2 Michael-Scott Lock-Free Queue  michael scott queue](5.4.2_Michael-Scott%20Lock-Free%20Queue_michael_scott_queue/index.md)
- [5.4.3 Bounded MPMC Array Queue  bounded mpmc array queue](5.4.3_Bounded%20MPMC%20Array%20Queue_bounded_mpmc_array_queue/index.md)
- [5.4.4 Per-Slot Sequence Number  per slot sequence number](5.4.4_Per-Slot%20Sequence%20Number_per_slot_sequence_number/index.md)
- [5.4.5 MPMC 的线性化点与正确性  mpmc linearization and correctness](5.4.5_MPMC%20%E7%9A%84%E7%BA%BF%E6%80%A7%E5%8C%96%E7%82%B9%E4%B8%8E%E6%AD%A3%E7%A1%AE%E6%80%A7_mpmc_linearization_and_correctness/index.md)
- [5.4.6 MPMC 的扩展性与热点分析  mpmc scalability and contention](5.4.6_MPMC%20%E7%9A%84%E6%89%A9%E5%B1%95%E6%80%A7%E4%B8%8E%E7%83%AD%E7%82%B9%E5%88%86%E6%9E%90_mpmc_scalability_and_contention/index.md)

## 导航

← 上一节：[5.3 MPSC 无锁队列  mpsc lock free queue](../5.3_MPSC%20无锁队列_mpsc_lock_free_queue/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.5 SPMC 与广播/扇出结构  spmc and broadcast queues](../5.5_SPMC%20与广播_扇出结构_spmc_and_broadcast_queues/index.md) →
