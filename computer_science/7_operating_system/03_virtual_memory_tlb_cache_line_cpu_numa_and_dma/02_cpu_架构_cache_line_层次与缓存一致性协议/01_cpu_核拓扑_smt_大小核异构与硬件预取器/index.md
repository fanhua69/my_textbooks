# 3.2.1 CPU 核拓扑、超线程（SMT）、大小核异构与硬件预取器

理解物理核/逻辑核资源共享、P-core/E-core 异构调度差异以及硬件预取器对访存模式的敏感性。

## 本节目录

- [3.2.1.1 物理核、SMT 超线程共享资源与 P-core / E-core 异构特性](01_物理核_smt_共享资源与大小核异构特性/index.md)
- [3.2.1.2 顺序/步长访存、指针追逐与硬件预取器（Hardware Prefetcher）](02_顺序_步长访存与硬件预取器行为/index.md)

---

## 导航

← 上一节：[3.1 虚拟地址空间、页表、TLB 与缺页异常（Page Fault）](../../01_虚拟地址空间_页表_tlb_与缺页异常/index.md)
↑ 返回上级：[3.2 CPU 架构、Cache Line 层次与缓存一致性协议](../index.md)
下一节：[3.2.2 L1i/L1d/L2/L3 Cache Line 原理、MESI/MOESI 一致性协议与伪共享（False Sharing）](../02_cache_line_mesi_moesi_一致性与伪共享/index.md) →
