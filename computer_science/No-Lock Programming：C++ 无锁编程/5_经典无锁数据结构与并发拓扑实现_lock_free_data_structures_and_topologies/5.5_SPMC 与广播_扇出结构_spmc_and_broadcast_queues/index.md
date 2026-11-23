# 5.5 SPMC 与广播/扇出结构  spmc and broadcast queues

研究一个生产者向多个消费者分发数据或广播事件的结构。

## 本节目录

- [5.5.1 SPMC 的任务分发语义  spmc work distribution](5.5.1_SPMC%20的任务分发语义_spmc_work_distribution/index.md)
- [5.5.2 SPMC 队列的消费者竞争  spmc consumer contention](5.5.2_SPMC%20队列的消费者竞争_spmc_consumer_contention/index.md)
- [5.5.3 Broadcast Queue 与 Fan-Out  broadcast queue and fanout](5.5.3_Broadcast%20Queue%20与%20Fan-Out_broadcast_queue_and_fanout/index.md)
- [5.5.4 多订阅者 Ring Buffer  multi subscriber ring buffer](5.5.4_多订阅者%20Ring%20Buffer_multi_subscriber_ring_buffer/index.md)
- [5.5.5 慢消费者、覆盖与背压  slow consumer and backpressure](5.5.5_慢消费者、覆盖与背压_slow_consumer_and_backpressure/index.md)

---

## 导航

← 上一节：[5.4 MPMC 无锁队列  mpmc lock free queue](../5.4_MPMC%20无锁队列_mpmc_lock_free_queue/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.6 其他常见无锁数据结构  other lock free data structures](../5.6_其他常见无锁数据结构_other_lock_free_data_structures/index.md) →
