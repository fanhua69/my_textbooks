# 3.3.3.1 伙伴系统、Slab/SLUB、大页（HugeTLB / 2MB / 1GB）与用户态分配器

**介绍**: 通过大页减少页表层级与 TLB Miss，对比分配器锁竞争与低延迟对象池/Arena 预分配。

---

## 导航

← 上一节：[3.3.2 Direct Access Memory：DMA、IOMMU/SMMU、缓存一致性与零拷贝通路](../../3.3.2_direct_access_memory_dma_iommu_与零拷贝通路/index.md)
↑ 返回上级：[3.3.3 内核/用户态内存分配器、大页（HugeTLB）与回收/淘汰机制](../index.md)
下一节：[3.3.3.2 后台回收、Swap、内存压缩与 OOM Killer / Jetsam 淘汰](../3.3.3.2_内存回收_swap_压缩与_oom_jetsam_机制/index.md) →
