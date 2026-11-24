# 5.5 SPMC 与广播/扇出结构  spmc and broadcast queues

**介绍**: 研究一个生产者向多个消费者分发数据或广播事件的结构。

## 目录

- [5.5.1 SPMC 的任务分发语义  spmc work distribution](5.5.1_SPMC%20%E7%9A%84%E4%BB%BB%E5%8A%A1%E5%88%86%E5%8F%91%E8%AF%AD%E4%B9%89_spmc_work_distribution/index.md)
- [5.5.2 SPMC 队列的消费者竞争  spmc consumer contention](5.5.2_SPMC%20%E9%98%9F%E5%88%97%E7%9A%84%E6%B6%88%E8%B4%B9%E8%80%85%E7%AB%9E%E4%BA%89_spmc_consumer_contention/index.md)
- [5.5.3 Broadcast Queue 与 Fan-Out  broadcast queue and fanout](5.5.3_Broadcast%20Queue%20%E4%B8%8E%20Fan-Out_broadcast_queue_and_fanout/index.md)
- [5.5.4 多订阅者 Ring Buffer  multi subscriber ring buffer](5.5.4_%E5%A4%9A%E8%AE%A2%E9%98%85%E8%80%85%20Ring%20Buffer_multi_subscriber_ring_buffer/index.md)
- [5.5.5 慢消费者、覆盖与背压  slow consumer and backpressure](5.5.5_慢消费者、覆盖与背压_slow_consumer_and_backpressure/index.md)

## 导航

← 上一节：[5.4 MPMC 无锁队列  mpmc lock free queue](../5.4_MPMC%20无锁队列_mpmc_lock_free_queue/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.6 其他常见无锁数据结构  other lock free data structures](../5.6_其他常见无锁数据结构_other_lock_free_data_structures/index.md) →
