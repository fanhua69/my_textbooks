# 1.4 无锁编程的适用边界  when to use lock free

**介绍**: 建立工程判断能力：理解无锁算法的收益、复杂度和维护成本，知道何时使用锁反而更好。

## 目录

- [1.4.1 无锁编程的收益与成本  benefits and costs](1.4.1_无锁编程的收益与成本_benefits_and_costs/index.md)
- [1.4.2 吞吐量、平均延迟与尾延迟  throughput latency and tail latency](1.4.2_吞吐量、平均延迟与尾延迟_throughput_latency_and_tail_latency/index.md)
- [1.4.3 锁、无锁与混合式设计的选择  lock vs lock free vs hybrid](1.4.3_锁、无锁与混合式设计的选择_lock_vs_lock_free_vs_hybrid/index.md)
- [1.4.4 无锁算法的典型应用领域  typical application domains](1.4.4_无锁算法的典型应用领域_typical_application_domains/index.md)

## 导航

← 上一节：[1.3 Lock-Free、Wait-Free 与进度保证  progress guarantees](../1.3_Lock-Free、Wait-Free%20与进度保证_progress_guarantees/index.md)
↑ 返回上级：[1 无锁编程基础与并发模型  lock free fundamentals and concurrency models](../index.md)
下一节：[2 CPU 原子操作、缓存一致性与硬件基础  hardware atomic operations and cache coherence](../../2_CPU%20原子操作、缓存一致性与硬件基础_hardware_atomic_operations_and_cache_coherence/index.md) →
