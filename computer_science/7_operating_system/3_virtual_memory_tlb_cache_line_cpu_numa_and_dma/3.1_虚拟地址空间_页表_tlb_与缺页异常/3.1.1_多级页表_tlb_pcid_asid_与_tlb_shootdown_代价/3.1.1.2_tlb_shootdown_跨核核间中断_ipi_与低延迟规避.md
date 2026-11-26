# 3.1.1.2 TLB Shootdown 跨核核间中断（IPI）与低延迟规避

**介绍**: 分析多线程频繁 mmap/munmap/mprotect 引发的核间中断抖动，通过预分配与池化规避。

---

## 导航

← 上一节：[3.1.1.1 4级/5级页表遍历、L1/L2 TLB 与 ASID / PCID 机制](../3.1.1.1_4级_5级页表遍历与_tlb_asid_pcid_机制/index.md)
↑ 返回上级：[3.1.1 多级页表遍历（Page Walk）、TLB 命中/失效、PCID/ASID 与 TLB Shootdown 代价](../index.md)
下一节：[3.1.2 Minor/Major Page Fault、写时复制（COW）与热路径防缺页](../../3.1.2_page_fault_cow_与热路径防缺页策略/index.md) →
