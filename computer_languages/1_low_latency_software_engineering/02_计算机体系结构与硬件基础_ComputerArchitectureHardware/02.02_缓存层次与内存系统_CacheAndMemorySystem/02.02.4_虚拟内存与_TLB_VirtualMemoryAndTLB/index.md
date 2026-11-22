# 2.2.4 虚拟内存与 TLB

地址转换开销常被低估，却是尾延迟的重要来源。

## 本节目录

- [2.2.4.1 页表遍历与 TLB 未命中](02.02.4.1_页表遍历与_TLB_未命中_PageWalkAndTLBMiss/index.md)
- [2.2.4.2 大页与透明大页](02.02.4.2_大页与透明大页_HugePages/index.md)
- [2.2.4.3 页面错误与缺页处理](02.02.4.3_页面错误与缺页处理_PageFaults/index.md)
- [2.2.4.4 TLB 击落](02.02.4.4_TLB_击落_TLBShootdown/index.md)

---

## 导航

← 上一节：[2.2.3 预取与内存级并行](../02.02.3_预取与内存级并行_PrefetchAndMLP/index.md)
↑ 返回上级：[2.2 缓存层次与内存系统](../index.md)
下一节：[2.2.5 NUMA 与内存拓扑](../02.02.5_NUMA_与内存拓扑_NUMAAndTopology/index.md) →
