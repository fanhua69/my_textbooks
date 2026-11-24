# 5.1 Ring Buffer 与循环队列  ring buffer and circular queue

**介绍**: 从数组环形缓冲区入手，理解无锁队列中索引、容量和缓存局部性。

## 目录

- [5.1.1 Ring Buffer 基本原理  ring buffer basics](5.1.1_Ring%20Buffer%20%E5%9F%BA%E6%9C%AC%E5%8E%9F%E7%90%86_ring_buffer_basics/index.md)
- [5.1.2 预留一个槽位的设计  one slot reservation](5.1.2_预留一个槽位的设计_one_slot_reservation/index.md)
- [5.1.3 计数器区分 Full 与 Empty  sequence counter full empty](5.1.3_%E8%AE%A1%E6%95%B0%E5%99%A8%E5%8C%BA%E5%88%86%20Full%20%E4%B8%8E%20Empty_sequence_counter_full_empty/index.md)
- [5.1.4 有界 SPSC Ring Buffer  bounded spsc ring buffer](5.1.4_%E6%9C%89%E7%95%8C%20SPSC%20Ring%20Buffer_bounded_spsc_ring_buffer/index.md)
- [5.1.5 Cache Line Padding 与索引隔离  cache line padding](5.1.5_Cache%20Line%20Padding%20%E4%B8%8E%E7%B4%A2%E5%BC%95%E9%9A%94%E7%A6%BB_cache_line_padding/index.md)
- [5.1.6 环形缓冲区的容量与溢出策略  capacity and overflow policy](5.1.6_环形缓冲区的容量与溢出策略_capacity_and_overflow_policy/index.md)

## 导航

← 上一节：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../../4_Lock-Free%20%E7%AE%97%E6%B3%95%E8%AE%BE%E8%AE%A1%E6%A0%B8%E5%BF%83%E6%8A%80%E6%9C%AF_lock_free_algorithm_design/index.md)
↑ 返回上级：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../index.md)
下一节：[5.2 SPSC 无锁队列  spsc lock free queue](../5.2_SPSC%20%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97_spsc_lock_free_queue/index.md) →
