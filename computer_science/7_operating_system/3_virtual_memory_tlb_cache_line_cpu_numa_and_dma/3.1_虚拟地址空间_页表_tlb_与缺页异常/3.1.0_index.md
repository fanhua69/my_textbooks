# 3.1 虚拟地址空间、页表、TLB 与缺页异常（Page Fault）

**介绍**: 消除热路径中的隐式缺页与 TLB 刷新抖动，掌握地址翻译缓存与内存映射/锁定原语。

## 目录

- [3.1.1 多级页表遍历（Page Walk）、TLB 命中/失效、PCID/ASID 与 TLB Shootdown 代价](3.1.1_多级页表_tlb_pcid_asid_与_tlb_shootdown_代价/index.md)
- [3.1.2 Minor/Major Page Fault、写时复制（COW）与热路径防缺页](3.1.2_page_fault_cow_与热路径防缺页策略/index.md)
- [3.1.3 mmap / munmap / madvise 与 Windows VirtualAlloc / VirtualProtect 对比](3.1.3_mmap_madvise_与_virtualalloc_语义对比/index.md)

## 导航

← 上一节：[2 内核架构、启动链路、进程与 Daemon/Service 托管](../../2_kernel_boot_processes_and_daemons/index.md)
↑ 返回上级：[3 虚拟内存、TLB、Cache Line、CPU、NUMA、DMA 与硬件内存体系](../index.md)
下一节：[3.2 CPU 架构、Cache Line 层次与缓存一致性协议](../3.2_cpu_架构_cache_line_层次与缓存一致性协议/index.md) →
