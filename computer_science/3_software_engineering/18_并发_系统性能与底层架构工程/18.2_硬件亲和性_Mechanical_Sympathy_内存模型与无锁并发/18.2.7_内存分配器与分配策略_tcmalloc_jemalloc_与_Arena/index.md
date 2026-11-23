# 18.2.7 内存分配器与分配策略：tcmalloc、jemalloc 与 Arena

分析 malloc 在多线程下的竞争与碎片问题，以线程缓存、Arena 与对象池优化分配热点。

---

## 导航

← 上一节：[18.2.6 NUMA 架构与 CPU 亲和性 (CPU Affinity)](../18.2.6_NUMA_架构与_CPU_亲和性_CPU_Affinity/index.md)
↑ 返回上级：[18.2 硬件亲和性 (Mechanical Sympathy)、内存模型与无锁并发](../index.md)
下一节：[18.3 高并发网络 I/O 模型与异步架构](../../18.3_高并发网络IO模型与异步架构/index.md) →
