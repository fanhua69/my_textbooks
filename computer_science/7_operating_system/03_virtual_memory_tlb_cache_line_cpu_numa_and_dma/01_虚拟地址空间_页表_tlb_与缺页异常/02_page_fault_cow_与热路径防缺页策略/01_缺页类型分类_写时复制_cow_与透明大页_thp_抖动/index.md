# 01 缺页类型分类、写时复制（COW）与透明大页（THP）抖动

**介绍**: 剖析磁盘 I/O 导致的 Major Fault、零页/COW 导致的 Minor Fault 以及 THP 合并/分裂带来的延迟尖峰。

---

## 导航

← 上一节：[3.1.1 多级页表遍历（Page Walk）、TLB 命中/失效、PCID/ASID 与 TLB Shootdown 代价](../../01_多级页表_tlb_pcid_asid_与_tlb_shootdown_代价/index.md)
↑ 返回上级：[3.1.2 Minor/Major Page Fault、写时复制（COW）与热路径防缺页](../index.md)
下一节：[3.1.2.2 mlock / mlockall / MAP POPULATE 与 VirtualLock 实践](../02_mlock_mlockall_map_populate_与_virtuallock_实践/index.md) →
