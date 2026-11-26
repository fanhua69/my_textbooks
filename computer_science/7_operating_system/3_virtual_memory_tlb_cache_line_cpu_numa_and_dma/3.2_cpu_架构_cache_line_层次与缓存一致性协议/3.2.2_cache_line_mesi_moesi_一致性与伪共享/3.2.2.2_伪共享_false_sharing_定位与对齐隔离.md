# 3.2.2.2 伪共享（False Sharing）成因、定位与 Cache Line 对齐隔离

**介绍**: 识别跨核高频写入不同变量却落在同一 Cache Line 的性能退化，使用 alignas 隔离热变量。

---

## 导航

← 上一节：[3.2.2.1 Cache Line 粒度、组相联映射、MESI/MOESI 状态机与缓冲队列](../3.2.2.1_cache_line_粒度_组相联与_mesi_moesi_状态机/index.md)
↑ 返回上级：[3.2.2 L1i/L1d/L2/L3 Cache Line 原理、MESI/MOESI 一致性协议与伪共享（False Sharing）](../index.md)
下一节：[3.2.3 指令缓存（I-Cache）、分支预测器与热点路径代码布局优化](../../3.2.3_指令缓存_分支预测与热点路径代码布局/index.md) →
