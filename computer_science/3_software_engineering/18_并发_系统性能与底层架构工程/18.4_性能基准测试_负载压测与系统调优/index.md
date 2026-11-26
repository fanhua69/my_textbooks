# 18.4 性能基准测试、负载压测与系统调优

**介绍**: 建立科学的系统性能实验方法论，准确定位并发瓶颈并实施架构级调优。


## 目录

- [18.4.1 延迟 (Latency)、吞吐量 (Throughput) 与尾延迟 (Tail Latency) 度量](18.4.1_延迟_Latency_吞吐量_Throughput_与尾延迟_Tail_Latency_度量.md)
- [18.4.2 基准测试 (Benchmark) 与并发负载压力测试](18.4.2_基准测试与并发负载压力测试_Benchmark.md)
- [18.4.3 压力测试与长时间浸泡稳定性测试 (Soak Testing)](18.4.3_压力测试与长时间浸泡稳定性测试_Soak_Testing.md)
- [18.4.4 全栈性能剖析 (Profiling) 与火焰图 (Flame Graphs) 调优](18.4.4_全栈性能剖析与火焰图调优_Profiling_Flame_Graphs.md)
- [18.4.5 内存剖析 (Memory Profiling)：堆分析、泄漏定位与分配热点](18.4.5_内存剖析_Memory_Profiling_堆分析_泄漏定位与分配热点.md)
- [18.4.6 缓存局部性与面向数据设计 (Data-Oriented Design)](18.4.6_缓存局部性与面向数据设计_Data-Oriented_Design.md)

---

## 导航

⬅️ 上一节：[18.3.2 Reactor 与 Proactor 高并发网络架构模式](../18.3_高并发网络IO模型与异步架构/18.3.2_Reactor与Proactor高并发网络架构模式.md)
⏺️ 当前节：[18.4 性能基准测试、负载压测与系统调优](index.md)
➡️ 下一节：[18.4.1 延迟 (Latency)、吞吐量 (Throughput) 与尾延迟 (Tail Latency) 度量](18.4.1_延迟_Latency_吞吐量_Throughput_与尾延迟_Tail_Latency_度量.md)
⬆️ 返回上级：[18 并发、系统性能与底层架构工程](../index.md)
