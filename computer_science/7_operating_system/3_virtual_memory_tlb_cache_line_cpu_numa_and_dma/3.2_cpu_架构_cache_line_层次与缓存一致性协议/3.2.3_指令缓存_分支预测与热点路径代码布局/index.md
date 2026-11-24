# 3.2.3 指令缓存（I-Cache）、分支预测器与热点路径代码布局优化

**介绍**: 减少热循环分支误预测与 I-Cache Miss，保持关键延迟路径紧凑、可预测、无堆分配。

## 目录

- [3.2.3.1 分支预测误判惩罚与冷热路径分离](3.2.3.1_分支预测误判惩罚与冷热路径分离/index.md)
- [3.2.3.2 指令缓存足迹控制、代码膨胀与热路径零分配/零异常](3.2.3.2_指令缓存足迹控制与热路径零分配设计/index.md)

## 导航

← 上一节：[3.2.2 L1i/L1d/L2/L3 Cache Line 原理、MESI/MOESI 一致性协议与伪共享（False Sharing）](../3.2.2_cache_line_mesi_moesi_一致性与伪共享/index.md)
↑ 返回上级：[3.2 CPU 架构、Cache Line 层次与缓存一致性协议](../index.md)
下一节：[3.3 NUMA 架构、Direct Access Memory（DMA / 零拷贝）与物理内存子系统](../../3.3_numa_direct_access_memory_dma_与物理内存子系统/index.md) →
