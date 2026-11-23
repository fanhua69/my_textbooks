# 3.3 3.3_Memory Order 六种内存序_memory_order

深入理解 relaxed、consume、acquire、release、acq_rel、seq_cst 的语义和适用场景。

## 本节目录

- [3.3.1 3.3.1_memory_order_relaxed_memory_order_relaxed](3.3.1_memory_order_relaxed_memory_order_relaxed/index.md)
- [3.3.2 3.3.2_memory_order_consume_memory_order_consume](3.3.2_memory_order_consume_memory_order_consume/index.md)
- [3.3.3 3.3.3_memory_order_acquire_memory_order_acquire](3.3.3_memory_order_acquire_memory_order_acquire/index.md)
- [3.3.4 3.3.4_memory_order_release_memory_order_release](3.3.4_memory_order_release_memory_order_release/index.md)
- [3.3.5 3.3.5_memory_order_acq_rel_memory_order_acq_rel](3.3.5_memory_order_acq_rel_memory_order_acq_rel/index.md)
- [3.3.6 3.3.6_memory_order_seq_cst_memory_order_seq_cst](3.3.6_memory_order_seq_cst_memory_order_seq_cst/index.md)
- [3.3.7 3.3.7_六种内存序对照与选择方法_memory_order_comparison](3.3.7_六种内存序对照与选择方法_memory_order_comparison/index.md)

---

## 导航

← 上一节：[3.2 3.2_std::atomic 全面介绍_std_atomic](../3.2_std__atomic 全面介绍_std_atomic/index.md)
↑ 返回上级：[3 3_C++ 原子库与内存模型_cpp_atomics_and_memory_model](../index.md)
下一节：[3.4 3.4_Fence、发布订阅与同步模式_fences_and_synchronization_patterns](../3.4_Fence、发布订阅与同步模式_fences_and_synchronization_patterns/index.md) →
