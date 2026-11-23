# 2.2 2.2_缓存一致性与多核通信_cache_coherence_and_intercore_communication

理解多个 CPU 核心如何观察共享缓存行，以及原子变量为何会成为性能热点。

## 本节目录

- [2.2.1 2.2.1_Cache Line 与缓存层次_cache_line_and_hierarchy](2.2.1_Cache Line 与缓存层次_cache_line_and_hierarchy/index.md)
- [2.2.2 2.2.2_MESI 与缓存一致性协议_mesi_and_cache_coherence](2.2.2_MESI 与缓存一致性协议_mesi_and_cache_coherence/index.md)
- [2.2.3 2.2.3_Cache Line Ping-Pong_cache_line_ping_pong](2.2.3_Cache Line Ping-Pong_cache_line_ping_pong/index.md)
- [2.2.4 2.2.4_False Sharing：伪共享_false_sharing](2.2.4_False Sharing：伪共享_false_sharing/index.md)
- [2.2.5 2.2.5_std::hardware_destructive_interference_size_hardware_destructive_interference_size](2.2.5_std__hardware_destructive_interference_size_hardware_destructive_interference_size/index.md)
- [2.2.6 2.2.6_NUMA 与跨插槽访问_numa_and_cross_socket_access](2.2.6_NUMA 与跨插槽访问_numa_and_cross_socket_access/index.md)

---

## 导航

← 上一节：[2.1 2.1_原子操作的硬件基础_hardware_atomic_primitives](../2.1_原子操作的硬件基础_hardware_atomic_primitives/index.md)
↑ 返回上级：[2 2_CPU 原子操作、缓存一致性与硬件基础_hardware_atomic_operations_and_cache_coherence](../index.md)
下一节：[2.3 2.3_内存屏障与处理器内存模型_hardware_memory_ordering](../2.3_内存屏障与处理器内存模型_hardware_memory_ordering/index.md) →
