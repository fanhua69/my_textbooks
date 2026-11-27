# 7.2 缓存与内存布局优化  cache and memory layout optimization

**介绍**: 从数据布局降低缓存未命中和跨核通信成本。

## 目录

- [7.2.1 Cache Locality 与 Data-Oriented Design  cache locality and data oriented design](7.2.1_Cache%20Locality%20%E4%B8%8E%20Data-Oriented%20Design_cache_locality_and_data_oriented_design/index.md)
- [7.2.2 Padding、Alignment 与 False Sharing  padding alignment and false sharing](7.2.2_Padding%E3%80%81Alignment%20%E4%B8%8E%20False%20Sharing_padding_alignment_and_false_sharing/index.md)
- [7.2.3 批处理与 Amortization  batching and amortization](7.2.3_%E6%89%B9%E5%A4%84%E7%90%86%E4%B8%8E%20Amortization_batching_and_amortization/index.md)
- [7.2.4 预分配与无动态分配路径  preallocation and allocation free path](7.2.4_预分配与无动态分配路径_preallocation_and_allocation_free_path/index.md)
- [7.2.5 Prefetch 与分支预测  prefetch and branch prediction](7.2.5_Prefetch%20%E4%B8%8E%E5%88%86%E6%94%AF%E9%A2%84%E6%B5%8B_prefetch_and_branch_prediction/index.md)

## 导航

← 上一节：[7.1 性能指标与基准测试  metrics and benchmarking](../7.1_性能指标与基准测试_metrics_and_benchmarking/index.md)
↑ 返回上级：[7 无锁编程性能工程与系统优化  lock free performance engineering](../index.md)
下一节：[7.3 线程调度与 NUMA 优化  thread scheduling and numa](../7.3_%E7%BA%BF%E7%A8%8B%E8%B0%83%E5%BA%A6%E4%B8%8E%20NUMA%20%E4%BC%98%E5%8C%96_thread_scheduling_and_numa/index.md) →
