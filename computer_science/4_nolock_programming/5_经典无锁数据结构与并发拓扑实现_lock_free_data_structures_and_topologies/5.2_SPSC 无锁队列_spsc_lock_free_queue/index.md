# 5.2 5.2_SPSC 无锁队列_spsc_lock_free_queue

深入实现最简单、常用于低延迟通道的单生产者单消费者队列。

## 本节目录

- [5.2.1 5.2.1_SPSC 的并发约束与所有权_spsc_constraints_and_ownership](5.2.1_SPSC 的并发约束与所有权_spsc_constraints_and_ownership/index.md)
- [5.2.2 5.2.2_SPSC 的 Release-Acquire 配对_spsc_release_acquire](5.2.2_SPSC 的 Release-Acquire 配对_spsc_release_acquire/index.md)
- [5.2.3 5.2.3_SPSC 入队与出队实现_spsc_enqueue_dequeue](5.2.3_SPSC 入队与出队实现_spsc_enqueue_dequeue/index.md)
- [5.2.4 5.2.4_SPSC 有界与无界实现比较_spsc_bounded_vs_unbounded](5.2.4_SPSC 有界与无界实现比较_spsc_bounded_vs_unbounded/index.md)
- [5.2.5 5.2.5_SPSC 批量读写与零拷贝_spsc_batch_and_zero_copy](5.2.5_SPSC 批量读写与零拷贝_spsc_batch_and_zero_copy/index.md)
- [5.2.6 5.2.6_SPSC 性能优化与适用场景_spsc_optimization_and_use_cases](5.2.6_SPSC 性能优化与适用场景_spsc_optimization_and_use_cases/index.md)

---

## 导航

← 上一节：[5.1 5.1_Ring Buffer 与循环队列_ring_buffer_and_circular_queue](../5.1_Ring Buffer 与循环队列_ring_buffer_and_circular_queue/index.md)
↑ 返回上级：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../index.md)
下一节：[5.3 5.3_MPSC 无锁队列_mpsc_lock_free_queue](../5.3_MPSC 无锁队列_mpsc_lock_free_queue/index.md) →
