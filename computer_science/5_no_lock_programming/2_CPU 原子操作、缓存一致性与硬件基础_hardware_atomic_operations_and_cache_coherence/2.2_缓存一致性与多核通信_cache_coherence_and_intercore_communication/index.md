# 2.2 缓存一致性与多核通信  cache coherence and intercore communication

理解多个 CPU 核心如何观察共享缓存行，以及原子变量为何会成为性能热点。

## 本节目录

- [2.2.1 Cache Line 与缓存层次  cache line and hierarchy](2.2.1_Cache%20Line%20与缓存层次_cache_line_and_hierarchy/index.md)
- [2.2.2 MESI 与缓存一致性协议  mesi and cache coherence](2.2.2_MESI%20与缓存一致性协议_mesi_and_cache_coherence/index.md)
- [2.2.3 Cache Line Ping-Pong  cache line ping pong](2.2.3_Cache%20Line%20Ping-Pong_cache_line_ping_pong/index.md)
- [2.2.4 False Sharing：伪共享  false sharing](2.2.4_False%20Sharing：伪共享_false_sharing/index.md)
- [2.2.5 std::hardware  destructive interference size hardware destructive interference size](2.2.5_std__hardware_destructive_interference_size_hardware_destructive_interference_size/index.md)
- [2.2.6 NUMA 与跨插槽访问  numa and cross socket access](2.2.6_NUMA%20与跨插槽访问_numa_and_cross_socket_access/index.md)

---

## 导航

← 上一节：[2.1 原子操作的硬件基础  hardware atomic primitives](../2.1_原子操作的硬件基础_hardware_atomic_primitives/index.md)
↑ 返回上级：[2 CPU 原子操作、缓存一致性与硬件基础  hardware atomic operations and cache coherence](../index.md)
下一节：[2.3 内存屏障与处理器内存模型  hardware memory ordering](../2.3_内存屏障与处理器内存模型_hardware_memory_ordering/index.md) →
