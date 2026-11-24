# 01 多级页表遍历（Page Walk）、TLB 命中/失效、PCID/ASID 与 TLB Shootdown 代价

**介绍**: 剖析多级页表遍历开销、TLB 大小与关联度限制、PCID/ASID 隔离以及跨核 TLB Shootdown 抖动。

## 目录

- [01 4级/5级页表遍历、L1/L2 TLB 与 ASID / PCID 机制](01_4级_5级页表遍历与_tlb_asid_pcid_机制/index.md)
- [02 TLB Shootdown 跨核核间中断（IPI）与低延迟规避](02_tlb_shootdown_跨核核间中断_ipi_与低延迟规避/index.md)

## 导航

← 上一节：[2 内核架构、启动链路、进程与 Daemon/Service 托管](../../../02_kernel_boot_processes_and_daemons/index.md)
↑ 返回上级：[3.1 虚拟地址空间、页表、TLB 与缺页异常（Page Fault）](../index.md)
下一节：[3.1.2 Minor/Major Page Fault、写时复制（COW）与热路径防缺页](../02_page_fault_cow_与热路径防缺页策略/index.md) →
