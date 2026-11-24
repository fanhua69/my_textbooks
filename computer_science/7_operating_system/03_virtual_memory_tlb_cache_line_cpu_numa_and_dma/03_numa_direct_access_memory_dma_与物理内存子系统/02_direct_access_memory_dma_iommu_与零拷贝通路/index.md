# 02 Direct Access Memory：DMA、IOMMU/SMMU、缓存一致性与零拷贝通路

**介绍**: 深入硬件直接内存访问（DMA）与总线/内存映射机制，消除 CPU 参与数据搬运的开销。

## 目录

- [01 DMA 控制器、Scatter-Gather、总线地址与 IOMMU / SMMU 地址转换](01_dma_原理_scatter_gather_与_iommu_smmu/index.md)
- [02 零拷贝 I/O、用户态映射与跨组件直接内存访问模式](02_零拷贝_i_o_用户态映射与直接内存访问模式/index.md)

## 导航

← 上一节：[3.3.1 NUMA 节点拓扑、跨节点访存延迟、内存策略与 macOS UMA 对比](../01_numa_拓扑_内存策略与_uma_对比/index.md)
↑ 返回上级：[3.3 NUMA 架构、Direct Access Memory（DMA / 零拷贝）与物理内存子系统](../index.md)
下一节：[3.3.3 内核/用户态内存分配器、大页（HugeTLB）与回收/淘汰机制](../03_内存分配器_大页与回收淘汰机制/index.md) →
