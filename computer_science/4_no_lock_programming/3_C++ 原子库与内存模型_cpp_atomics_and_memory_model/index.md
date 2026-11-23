# 3 C++ 原子库与内存模型  cpp atomics and memory model

系统掌握 C++11 引入的内存模型与原子库，并追踪 C++14/17/20/23/26 的相关演进。重点理解 memory_order、happens-before 和正确发布数据的方式。

## 本节目录

- [3.1 C++ 并发内存模型  cpp concurrency memory model](3.1_C++%20并发内存模型_cpp_concurrency_memory_model/index.md)
- [3.2 std::atomic 全面介绍  std atomic](3.2_std__atomic%20全面介绍_std_atomic/index.md)
- [3.3 Memory Order 六种内存序  memory order](3.3_Memory%20Order%20六种内存序_memory_order/index.md)
- [3.4 Fence、发布订阅与同步模式  fences and synchronization patterns](3.4_Fence、发布订阅与同步模式_fences_and_synchronization_patterns/index.md)
- [3.5 C++ 标准演进与并发设施  cpp standard evolution](3.5_C++%20标准演进与并发设施_cpp_standard_evolution/index.md)

---

## 导航

← 上一节：[2 CPU 原子操作、缓存一致性与硬件基础  hardware atomic operations and cache coherence](../2_CPU%20原子操作、缓存一致性与硬件基础_hardware_atomic_operations_and_cache_coherence/index.md)
↑ 返回上级：[No-Lock Programming：C++ 无锁编程](../index.md)
下一节：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../4_Lock-Free%20算法设计核心技术_lock_free_algorithm_design/index.md) →
