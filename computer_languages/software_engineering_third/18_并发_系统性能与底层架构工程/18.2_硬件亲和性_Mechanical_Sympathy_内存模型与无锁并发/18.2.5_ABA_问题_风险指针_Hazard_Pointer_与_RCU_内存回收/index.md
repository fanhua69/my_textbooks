# 18.2.5 ABA 问题、风险指针 (Hazard Pointer) 与 RCU 内存回收

分析无锁结构中 ABA 与安全内存回收难题，对比带标记指针、风险指针与 RCU 的解决方案。

---

## 导航

← 上一节：[18.2.4 无锁数据结构：无锁栈、无锁队列与 SPSC / MPSC / SPMC / MPMC](../18.2.4_无锁数据结构_无锁栈_无锁队列与_SPSC_MPSC_SPMC_MPMC/index.md)
↑ 返回上级：[18.2 硬件亲和性 (Mechanical Sympathy)、内存模型与无锁并发](../index.md)
下一节：[18.2.6 NUMA 架构与 CPU 亲和性 (CPU Affinity)](../18.2.6_NUMA_架构与_CPU_亲和性_CPU_Affinity/index.md) →
