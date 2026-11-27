# 5.2 SPSC 无锁队列  spsc lock free queue

**介绍**: 深入实现最简单、常用于低延迟通道的单生产者单消费者队列。

## 目录

- [5.2.1 SPSC 的并发约束与所有权  spsc constraints and ownership](5.2.1_SPSC%20%E7%9A%84%E5%B9%B6%E5%8F%91%E7%BA%A6%E6%9D%9F%E4%B8%8E%E6%89%80%E6%9C%89%E6%9D%83_spsc_constraints_and_ownership/index.md)
- [5.2.2 SPSC 的 Release-Acquire 配对  spsc release acquire](5.2.2_SPSC%20%E7%9A%84%20Release-Acquire%20%E9%85%8D%E5%AF%B9_spsc_release_acquire/index.md)
- [5.2.3 SPSC 入队与出队实现  spsc enqueue dequeue](5.2.3_SPSC%20%E5%85%A5%E9%98%9F%E4%B8%8E%E5%87%BA%E9%98%9F%E5%AE%9E%E7%8E%B0_spsc_enqueue_dequeue/index.md)
- [5.2.4 SPSC 有界与无界实现比较  spsc bounded vs unbounded](5.2.4_SPSC%20%E6%9C%89%E7%95%8C%E4%B8%8E%E6%97%A0%E7%95%8C%E5%AE%9E%E7%8E%B0%E6%AF%94%E8%BE%83_spsc_bounded_vs_unbounded/index.md)
- [5.2.5 SPSC 批量读写与零拷贝  spsc batch and zero copy](5.2.5_SPSC%20%E6%89%B9%E9%87%8F%E8%AF%BB%E5%86%99%E4%B8%8E%E9%9B%B6%E6%8B%B7%E8%B4%9D_spsc_batch_and_zero_copy/index.md)
- [5.2.6 SPSC 性能优化与适用场景  spsc optimization and use cases](5.2.6_SPSC%20%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96%E4%B8%8E%E9%80%82%E7%94%A8%E5%9C%BA%E6%99%AF_spsc_optimization_and_use_cases/index.md)

## 导航

← 上一节：[5.1 Ring Buffer 与循环队列  ring buffer and circular queue](../5.1_Ring%20Buffer%20%E4%B8%8E%E5%BE%AA%E7%8E%AF%E9%98%9F%E5%88%97_ring_buffer_and_circular_queue/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.3 MPSC 无锁队列  mpsc lock free queue](../5.3_MPSC%20%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97_mpsc_lock_free_queue/index.md) →
