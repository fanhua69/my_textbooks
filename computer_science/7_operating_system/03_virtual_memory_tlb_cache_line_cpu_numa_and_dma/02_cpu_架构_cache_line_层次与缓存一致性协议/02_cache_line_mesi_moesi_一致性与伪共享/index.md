# 3.2.2 L1i/L1d/L2/L3 Cache Line 原理、MESI/MOESI 一致性协议与伪共享（False Sharing）

深入 Cache Line 大小、组相联映射、缓存一致性状态机与伪共享根因及隔离手段。

## 本节目录

- [3.2.2.1 Cache Line 粒度、组相联映射、MESI/MOESI 状态机与缓冲队列](01_cache_line_粒度_组相联与_mesi_moesi_状态机/index.md)
- [3.2.2.2 伪共享（False Sharing）成因、定位与 Cache Line 对齐隔离](02_伪共享_false_sharing_定位与对齐隔离/index.md)

---

## 导航

← 上一节：[3.2.1 CPU 核拓扑、超线程（SMT）、大小核异构与硬件预取器](../01_cpu_核拓扑_smt_大小核异构与硬件预取器/index.md)
↑ 返回上级：[3.2 CPU 架构、Cache Line 层次与缓存一致性协议](../index.md)
下一节：[3.2.3 指令缓存（I-Cache）、分支预测器与热点路径代码布局优化](../03_指令缓存_分支预测与热点路径代码布局/index.md) →
