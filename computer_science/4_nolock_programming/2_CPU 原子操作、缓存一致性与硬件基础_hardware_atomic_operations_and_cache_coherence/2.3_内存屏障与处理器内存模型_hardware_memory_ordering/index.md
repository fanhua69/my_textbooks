# 2.3 2.3_内存屏障与处理器内存模型_hardware_memory_ordering

理解编译器和 CPU 为什么会重排内存操作，以及屏障如何约束可观察顺序。

## 本节目录

- [2.3.1 2.3.1_编译器重排与 CPU 重排_compiler_and_cpu_reordering](2.3.1_编译器重排与 CPU 重排_compiler_and_cpu_reordering/index.md)
- [2.3.2 2.3.2_Store Buffer 与 Load Buffer_store_buffer_and_load_buffer](2.3.2_Store Buffer 与 Load Buffer_store_buffer_and_load_buffer/index.md)
- [2.3.3 2.3.3_Memory Fence 与 Barrier_memory_fence_and_barrier](2.3.3_Memory Fence 与 Barrier_memory_fence_and_barrier/index.md)
- [2.3.4 2.3.4_x86-TSO 与 ARM 弱内存模型_x86_tso_and_arm_weak_memory_model](2.3.4_x86-TSO 与 ARM 弱内存模型_x86_tso_and_arm_weak_memory_model/index.md)
- [2.3.5 2.3.5_原子操作的硬件代价_cost_of_atomic_operations](2.3.5_原子操作的硬件代价_cost_of_atomic_operations/index.md)

---

## 导航

← 上一节：[2.2 2.2_缓存一致性与多核通信_cache_coherence_and_intercore_communication](../2.2_缓存一致性与多核通信_cache_coherence_and_intercore_communication/index.md)
↑ 返回上级：[2 2_CPU 原子操作、缓存一致性与硬件基础_hardware_atomic_operations_and_cache_coherence](../index.md)
下一节：[3 3_C++ 原子库与内存模型_cpp_atomics_and_memory_model](../../3_C++ 原子库与内存模型_cpp_atomics_and_memory_model/index.md) →
