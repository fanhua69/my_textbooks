# 3.1.2 Minor/Major Page Fault、写时复制（COW）与热路径防缺页

理解按需调页与 COW 在低延迟路径中的延迟毛刺成因，掌握内存预 fault、锁定物理页与禁用透明大页毛刺的方法。

## 本节目录

- [3.1.2.1 缺页类型分类、写时复制（COW）与透明大页（THP）抖动](01_缺页类型分类_写时复制_cow_与透明大页_thp_抖动/index.md)
- [3.1.2.2 mlock / mlockall / MAP POPULATE 与 VirtualLock 实践](02_mlock_mlockall_map_populate_与_virtuallock_实践/index.md)

---

## 导航

← 上一节：[3.1.1 多级页表遍历（Page Walk）、TLB 命中/失效、PCID/ASID 与 TLB Shootdown 代价](../01_多级页表_tlb_pcid_asid_与_tlb_shootdown_代价/index.md)
↑ 返回上级：[3.1 虚拟地址空间、页表、TLB 与缺页异常（Page Fault）](../index.md)
下一节：[3.1.3 mmap / munmap / madvise 与 Windows VirtualAlloc / VirtualProtect 对比](../03_mmap_madvise_与_virtualalloc_语义对比/index.md) →
