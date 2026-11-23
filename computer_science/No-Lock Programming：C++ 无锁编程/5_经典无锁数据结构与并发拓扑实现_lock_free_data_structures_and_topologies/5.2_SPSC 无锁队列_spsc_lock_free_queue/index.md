# 5.2 SPSC 无锁队列  spsc lock free queue

深入实现最简单、常用于低延迟通道的单生产者单消费者队列。

## 本节目录

- [5.2.1 SPSC 的并发约束与所有权  spsc constraints and ownership](5.2.1_SPSC%20的并发约束与所有权_spsc_constraints_and_ownership/index.md)
- [5.2.2 SPSC 的 Release-Acquire 配对  spsc release acquire](5.2.2_SPSC%20的%20Release-Acquire%20配对_spsc_release_acquire/index.md)
- [5.2.3 SPSC 入队与出队实现  spsc enqueue dequeue](5.2.3_SPSC%20入队与出队实现_spsc_enqueue_dequeue/index.md)
- [5.2.4 SPSC 有界与无界实现比较  spsc bounded vs unbounded](5.2.4_SPSC%20有界与无界实现比较_spsc_bounded_vs_unbounded/index.md)
- [5.2.5 SPSC 批量读写与零拷贝  spsc batch and zero copy](5.2.5_SPSC%20批量读写与零拷贝_spsc_batch_and_zero_copy/index.md)
- [5.2.6 SPSC 性能优化与适用场景  spsc optimization and use cases](5.2.6_SPSC%20性能优化与适用场景_spsc_optimization_and_use_cases/index.md)

---

## 导航

← 上一节：[5.1 Ring Buffer 与循环队列  ring buffer and circular queue](../5.1_Ring%20Buffer%20与循环队列_ring_buffer_and_circular_queue/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.3 MPSC 无锁队列  mpsc lock free queue](../5.3_MPSC%20无锁队列_mpsc_lock_free_queue/index.md) →
