# 01 DMA 控制器、Scatter-Gather、总线地址与 IOMMU / SMMU 地址转换

**介绍**: 理解外设直接读写物理内存的机制、IOMMU 隔离与地址重映射及 DMA 缓冲一致性同步。

---

## 导航

← 上一节：[3.3.1 NUMA 节点拓扑、跨节点访存延迟、内存策略与 macOS UMA 对比](../../01_numa_拓扑_内存策略与_uma_对比/index.md)
↑ 返回上级：[3.3.2 Direct Access Memory：DMA、IOMMU/SMMU、缓存一致性与零拷贝通路](../index.md)
下一节：[3.3.2.2 零拷贝 I/O、用户态映射与跨组件直接内存访问模式](../02_零拷贝_i_o_用户态映射与直接内存访问模式/index.md) →
