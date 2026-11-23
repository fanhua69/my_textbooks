# 5.5 5.5_SPMC 与广播/扇出结构_spmc_and_broadcast_queues

研究一个生产者向多个消费者分发数据或广播事件的结构。

## 本节目录

- [5.5.1 5.5.1_SPMC 的任务分发语义_spmc_work_distribution](5.5.1_SPMC 的任务分发语义_spmc_work_distribution/index.md)
- [5.5.2 5.5.2_SPMC 队列的消费者竞争_spmc_consumer_contention](5.5.2_SPMC 队列的消费者竞争_spmc_consumer_contention/index.md)
- [5.5.3 5.5.3_Broadcast Queue 与 Fan-Out_broadcast_queue_and_fanout](5.5.3_Broadcast Queue 与 Fan-Out_broadcast_queue_and_fanout/index.md)
- [5.5.4 5.5.4_多订阅者 Ring Buffer_multi_subscriber_ring_buffer](5.5.4_多订阅者 Ring Buffer_multi_subscriber_ring_buffer/index.md)
- [5.5.5 5.5.5_慢消费者、覆盖与背压_slow_consumer_and_backpressure](5.5.5_慢消费者、覆盖与背压_slow_consumer_and_backpressure/index.md)

---

## 导航

← 上一节：[5.4 5.4_MPMC 无锁队列_mpmc_lock_free_queue](../5.4_MPMC 无锁队列_mpmc_lock_free_queue/index.md)
↑ 返回上级：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../index.md)
下一节：[5.6 5.6_其他常见无锁数据结构_other_lock_free_data_structures](../5.6_其他常见无锁数据结构_other_lock_free_data_structures/index.md) →
