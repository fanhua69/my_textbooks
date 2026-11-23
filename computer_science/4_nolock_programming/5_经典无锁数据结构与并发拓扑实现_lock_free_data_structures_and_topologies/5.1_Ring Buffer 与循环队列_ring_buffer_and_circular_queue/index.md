# 5.1 5.1_Ring Buffer 与循环队列_ring_buffer_and_circular_queue

从数组环形缓冲区入手，理解无锁队列中索引、容量和缓存局部性。

## 本节目录

- [5.1.1 5.1.1_Ring Buffer 基本原理_ring_buffer_basics](5.1.1_Ring Buffer 基本原理_ring_buffer_basics/index.md)
- [5.1.2 5.1.2_预留一个槽位的设计_one_slot_reservation](5.1.2_预留一个槽位的设计_one_slot_reservation/index.md)
- [5.1.3 5.1.3_计数器区分 Full 与 Empty_sequence_counter_full_empty](5.1.3_计数器区分 Full 与 Empty_sequence_counter_full_empty/index.md)
- [5.1.4 5.1.4_有界 SPSC Ring Buffer_bounded_spsc_ring_buffer](5.1.4_有界 SPSC Ring Buffer_bounded_spsc_ring_buffer/index.md)
- [5.1.5 5.1.5_Cache Line Padding 与索引隔离_cache_line_padding](5.1.5_Cache Line Padding 与索引隔离_cache_line_padding/index.md)
- [5.1.6 5.1.6_环形缓冲区的容量与溢出策略_capacity_and_overflow_policy](5.1.6_环形缓冲区的容量与溢出策略_capacity_and_overflow_policy/index.md)

---

## 导航

← 上一节：[4 4_Lock-Free 算法设计核心技术_lock_free_algorithm_design](../../4_Lock-Free 算法设计核心技术_lock_free_algorithm_design/index.md)
↑ 返回上级：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../index.md)
下一节：[5.2 5.2_SPSC 无锁队列_spsc_lock_free_queue](../5.2_SPSC 无锁队列_spsc_lock_free_queue/index.md) →
