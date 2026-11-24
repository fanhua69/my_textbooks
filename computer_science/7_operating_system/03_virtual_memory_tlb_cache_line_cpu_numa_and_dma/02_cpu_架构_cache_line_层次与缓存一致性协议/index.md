# 02 CPU 架构、Cache Line 层次与缓存一致性协议

**介绍**: 将数据结构、线程布局与并发原语对齐到 CPU 核拓扑与 Cache Line，消除伪共享、缓存行乒乓与流水线/访存抖动。

## 目录

- [01 CPU 核拓扑、超线程（SMT）、大小核异构与硬件预取器](01_cpu_核拓扑_smt_大小核异构与硬件预取器/index.md)
- [02 L1i/L1d/L2/L3 Cache Line 原理、MESI/MOESI 一致性协议与伪共享（False Sharing）](02_cache_line_mesi_moesi_一致性与伪共享/index.md)
- [03 指令缓存（I-Cache）、分支预测器与热点路径代码布局优化](03_指令缓存_分支预测与热点路径代码布局/index.md)

## 导航

← 上一节：[3.1 虚拟地址空间、页表、TLB 与缺页异常（Page Fault）](../01_虚拟地址空间_页表_tlb_与缺页异常/index.md)
↑ 返回上级：[3 虚拟内存、TLB、Cache Line、CPU、NUMA、DMA 与硬件内存体系](../index.md)
下一节：[3.3 NUMA 架构、Direct Access Memory（DMA / 零拷贝）与物理内存子系统](../03_numa_direct_access_memory_dma_与物理内存子系统/index.md) →
