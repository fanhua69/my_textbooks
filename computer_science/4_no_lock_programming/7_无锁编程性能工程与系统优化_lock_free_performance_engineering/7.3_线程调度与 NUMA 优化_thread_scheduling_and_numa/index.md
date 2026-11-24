# 7.3 线程调度与 NUMA 优化  thread scheduling and numa

**介绍**: 理解操作系统调度和硬件拓扑对无锁算法的影响。

## 目录

- [7.3.1 CPU Affinity 与线程绑核  cpu affinity](7.3.1_CPU%20Affinity%20%E4%B8%8E%E7%BA%BF%E7%A8%8B%E7%BB%91%E6%A0%B8_cpu_affinity/index.md)
- [7.3.2 NUMA-aware 数据结构  numa aware data structures](7.3.2_NUMA-aware%20%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84_numa_aware_data_structures/index.md)
- [7.3.3 SMT/Hyper-Threading 的影响  smt and hyper threading](7.3.3_SMT_Hyper-Threading%20%E7%9A%84%E5%BD%B1%E5%93%8D_smt_and_hyper_threading/index.md)
- [7.3.4 优先级、抢占与实时调度  priority preemption and realtime scheduling](7.3.4_优先级、抢占与实时调度_priority_preemption_and_realtime_scheduling/index.md)
- [7.3.5 忙等、pause 与自适应等待  spin pause and adaptive waiting](7.3.5_%E5%BF%99%E7%AD%89%E3%80%81pause%20%E4%B8%8E%E8%87%AA%E9%80%82%E5%BA%94%E7%AD%89%E5%BE%85_spin_pause_and_adaptive_waiting/index.md)

## 导航

← 上一节：[7.2 缓存与内存布局优化  cache and memory layout optimization](../7.2_缓存与内存布局优化_cache_and_memory_layout_optimization/index.md)
↑ 返回上级：[7 无锁编程性能工程与系统优化  lock free performance engineering](../index.md)
下一节：[7.4 低延迟系统中的无锁设计  lock free for low latency systems](../7.4_低延迟系统中的无锁设计_lock_free_for_low_latency_systems/index.md) →
