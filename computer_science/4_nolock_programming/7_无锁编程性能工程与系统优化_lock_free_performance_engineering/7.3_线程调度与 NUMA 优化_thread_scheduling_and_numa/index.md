# 7.3 7.3_线程调度与 NUMA 优化_thread_scheduling_and_numa

理解操作系统调度和硬件拓扑对无锁算法的影响。

## 本节目录

- [7.3.1 7.3.1_CPU Affinity 与线程绑核_cpu_affinity](7.3.1_CPU Affinity 与线程绑核_cpu_affinity/index.md)
- [7.3.2 7.3.2_NUMA-aware 数据结构_numa_aware_data_structures](7.3.2_NUMA-aware 数据结构_numa_aware_data_structures/index.md)
- [7.3.3 7.3.3_SMT/Hyper-Threading 的影响_smt_and_hyper_threading](7.3.3_SMT_Hyper-Threading 的影响_smt_and_hyper_threading/index.md)
- [7.3.4 7.3.4_优先级、抢占与实时调度_priority_preemption_and_realtime_scheduling](7.3.4_优先级、抢占与实时调度_priority_preemption_and_realtime_scheduling/index.md)
- [7.3.5 7.3.5_忙等、pause 与自适应等待_spin_pause_and_adaptive_waiting](7.3.5_忙等、pause 与自适应等待_spin_pause_and_adaptive_waiting/index.md)

---

## 导航

← 上一节：[7.2 7.2_缓存与内存布局优化_cache_and_memory_layout_optimization](../7.2_缓存与内存布局优化_cache_and_memory_layout_optimization/index.md)
↑ 返回上级：[7 7_无锁编程性能工程与系统优化_lock_free_performance_engineering](../index.md)
下一节：[7.4 7.4_低延迟系统中的无锁设计_lock_free_for_low_latency_systems](../7.4_低延迟系统中的无锁设计_lock_free_for_low_latency_systems/index.md) →
