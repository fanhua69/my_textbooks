# 5.3 MPSC 无锁队列  mpsc lock free queue

**介绍**: 研究多个生产者并发提交、单消费者串行处理的结构。

## 目录

- [5.3.1 MPSC 的并发约束与典型场景  mpsc constraints and use cases](5.3.1_MPSC%20%E7%9A%84%E5%B9%B6%E5%8F%91%E7%BA%A6%E6%9D%9F%E4%B8%8E%E5%85%B8%E5%9E%8B%E5%9C%BA%E6%99%AF_mpsc_constraints_and_use_cases/index.md)
- [5.3.2 基于 CAS 的 MPSC 入队  mpsc cas enqueue](5.3.2_%E5%9F%BA%E4%BA%8E%20CAS%20%E7%9A%84%20MPSC%20%E5%85%A5%E9%98%9F_mpsc_cas_enqueue/index.md)
- [5.3.3 单消费者出队路径  mpsc single consumer dequeue](5.3.3_单消费者出队路径_mpsc_single_consumer_dequeue/index.md)
- [5.3.4 Intrusive MPSC Queue  intrusive mpsc queue](5.3.4_Intrusive%20MPSC%20Queue_intrusive_mpsc_queue/index.md)
- [5.3.5 MPSC 的空队列与链表断链窗口  mpsc empty and linking window](5.3.5_MPSC%20%E7%9A%84%E7%A9%BA%E9%98%9F%E5%88%97%E4%B8%8E%E9%93%BE%E8%A1%A8%E6%96%AD%E9%93%BE%E7%AA%97%E5%8F%A3_mpsc_empty_and_linking_window/index.md)
- [5.3.6 MPSC 有界队列与序列号方案  bounded mpsc sequence queue](5.3.6_MPSC%20%E6%9C%89%E7%95%8C%E9%98%9F%E5%88%97%E4%B8%8E%E5%BA%8F%E5%88%97%E5%8F%B7%E6%96%B9%E6%A1%88_bounded_mpsc_sequence_queue/index.md)

## 导航

← 上一节：[5.2 SPSC 无锁队列  spsc lock free queue](../5.2_SPSC%20%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97_spsc_lock_free_queue/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.4 MPMC 无锁队列  mpmc lock free queue](../5.4_MPMC%20%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97_mpmc_lock_free_queue/index.md) →
