# 1.2 1.2_并发拓扑与生产者消费者模型_concurrency_topologies

以生产者和消费者的数量关系为主线，系统介绍 SPSC、SPMC、MPSC、MPMC 等常见并发拓扑。这些拓扑是选择队列、环形缓冲区和任务调度结构的基础。

## 本节目录

- [1.2.1 1.2.1_生产者与消费者模型概览_producer_consumer_model_overview](1.2.1_生产者与消费者模型概览_producer_consumer_model_overview/index.md)
- [1.2.2 1.2.2_SPSC：Single Producer Single Consumer_spsc_single_producer_single_consumer](1.2.2_SPSC：Single Producer Single Consumer_spsc_single_producer_single_consumer/index.md)
- [1.2.3 1.2.3_SPMC：Single Producer Multiple Consumers_spmc_single_producer_multiple_consumers](1.2.3_SPMC：Single Producer Multiple Consumers_spmc_single_producer_multiple_consumers/index.md)
- [1.2.4 1.2.4_MPSC：Multiple Producers Single Consumer_mpsc_multiple_producers_single_consumer](1.2.4_MPSC：Multiple Producers Single Consumer_mpsc_multiple_producers_single_consumer/index.md)
- [1.2.5 1.2.5_MPMC：Multiple Producers Multiple Consumers_mpmc_multiple_producers_multiple_consumers](1.2.5_MPMC：Multiple Producers Multiple Consumers_mpmc_multiple_producers_multiple_consumers/index.md)
- [1.2.6 1.2.6_模型对比：SPSC、SPMC、MPSC 与 MPMC_compare_spsc_spmc_mpsc_mpmc](1.2.6_模型对比：SPSC、SPMC、MPSC 与 MPMC_compare_spsc_spmc_mpsc_mpmc/index.md)
- [1.2.7 1.2.7_扩展拓扑：N-to-1、1-to-N 与 N-to-M_extended_producer_consumer_topologies](1.2.7_扩展拓扑：N-to-1、1-to-N 与 N-to-M_extended_producer_consumer_topologies/index.md)
- [1.2.8 1.2.8_有界与无界队列_bounded_and_unbounded_queues](1.2.8_有界与无界队列_bounded_and_unbounded_queues/index.md)

---

## 导航

← 上一节：[1.1 1.1_并发基础与同步原语_concurrency_fundamentals](../1.1_并发基础与同步原语_concurrency_fundamentals/index.md)
↑ 返回上级：[1 1_无锁编程基础与并发模型_lock_free_fundamentals_and_concurrency_models](../index.md)
下一节：[1.3 1.3_Lock-Free、Wait-Free 与进度保证_progress_guarantees](../1.3_Lock-Free、Wait-Free 与进度保证_progress_guarantees/index.md) →
