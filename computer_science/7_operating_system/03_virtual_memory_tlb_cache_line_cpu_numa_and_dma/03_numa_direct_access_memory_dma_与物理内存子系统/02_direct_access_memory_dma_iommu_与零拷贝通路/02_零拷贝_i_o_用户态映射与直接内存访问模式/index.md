# 3.3.2.2 零拷贝 I/O、用户态映射与跨组件直接内存访问模式

对比传统多次拷贝路径与固定缓冲区 DMA / 共享内存零拷贝在吞吐与延迟上的收益与约束。

---

## 导航

← 上一节：[3.3.2.1 DMA 控制器、Scatter-Gather、总线地址与 IOMMU / SMMU 地址转换](../01_dma_原理_scatter_gather_与_iommu_smmu/index.md)
↑ 返回上级：[3.3.2 Direct Access Memory：DMA、IOMMU/SMMU、缓存一致性与零拷贝通路](../index.md)
下一节：[3.3.3 内核/用户态内存分配器、大页（HugeTLB）与回收/淘汰机制](../../03_内存分配器_大页与回收淘汰机制/index.md) →
