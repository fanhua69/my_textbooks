# 3.3.3 内核/用户态内存分配器、大页（HugeTLB）与回收/淘汰机制

掌握伙伴系统、Slab/SLUB、用户态分配器、大页 TLB 覆盖率提升以及内存回收/OOM/Jetsam 策略。

## 本节目录

- [3.3.3.1 伙伴系统、Slab/SLUB、大页（HugeTLB / 2MB / 1GB）与用户态分配器](01_分配器层次_大页配置与预分配策略/index.md)
- [3.3.3.2 后台回收、Swap、内存压缩与 OOM Killer / Jetsam 淘汰](02_内存回收_swap_压缩与_oom_jetsam_机制/index.md)

---

## 导航

← 上一节：[3.3.2 Direct Access Memory：DMA、IOMMU/SMMU、缓存一致性与零拷贝通路](../02_direct_access_memory_dma_iommu_与零拷贝通路/index.md)
↑ 返回上级：[3.3 NUMA 架构、Direct Access Memory（DMA / 零拷贝）与物理内存子系统](../index.md)
下一节：[4 进程间通信（IPC）、共享内存与高速数据通道](../../../04_ipc_shared_memory_and_data_channels/index.md) →
