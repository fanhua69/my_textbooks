# 3.1.1.1 4级/5级页表遍历、L1/L2 TLB 与 ASID / PCID 机制

**介绍**: 理解地址空间标识符如何减少上下文切换时的全量 TLB 刷写，以及页表 walk 对访存延迟的放大。

---

## 导航

← 上一节：[2 内核架构、启动链路、进程与 Daemon/Service 托管](../../../../2_kernel_boot_processes_and_daemons/index.md)
↑ 返回上级：[3.1.1 多级页表遍历（Page Walk）、TLB 命中/失效、PCID/ASID 与 TLB Shootdown 代价](../index.md)
下一节：[3.1.1.2 TLB Shootdown 跨核核间中断（IPI）与低延迟规避](../3.1.1.2_tlb_shootdown_跨核核间中断_ipi_与低延迟规避/index.md) →
