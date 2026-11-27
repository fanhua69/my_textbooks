# 3.3 NUMA 架构、Direct Access Memory（DMA / 零拷贝）与物理内存子系统

**介绍**: 掌握多 Socket NUMA 拓扑、Direct Access Memory（DMA / IOMMU / GPUDirect / 共享内存零拷贝）以及内核/用户态内存分配与回收机制。

## 目录

- [3.3.1 NUMA 节点拓扑、跨节点访存延迟、内存策略与 macOS UMA 对比](3.3.1_numa_拓扑_内存策略与_uma_对比/index.md)
- [3.3.2 Direct Access Memory：DMA、IOMMU/SMMU、缓存一致性与零拷贝通路](3.3.2_direct_access_memory_dma_iommu_与零拷贝通路/index.md)
- [3.3.3 内核/用户态内存分配器、大页（HugeTLB）与回收/淘汰机制](3.3.3_内存分配器_大页与回收淘汰机制/index.md)

## 导航

← 上一节：[3.2 CPU 架构、Cache Line 层次与缓存一致性协议](../3.2_cpu_架构_cache_line_层次与缓存一致性协议/index.md)
↑ 返回上级：[3 虚拟内存、TLB、Cache Line、CPU、NUMA、DMA 与硬件内存体系](../index.md)
下一节：[4 进程间通信（IPC）、共享内存与高速数据通道](../../4_ipc_shared_memory_and_data_channels/index.md) →
