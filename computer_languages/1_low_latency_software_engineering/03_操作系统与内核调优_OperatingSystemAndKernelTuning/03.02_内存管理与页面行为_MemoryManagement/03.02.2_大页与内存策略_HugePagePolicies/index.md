# 3.2.2 大页与内存策略

在可控前提下使用大页降低 TLB 压力。

## 本节目录

- [3.2.2.1 显式大页 hugetlbfs 与 1GB 页](03.02.2.1_显式大页_hugetlbfs_与_1GB_页_Hugetlbfs/index.md)
- [3.2.2.2 THP 的利弊与关闭](03.02.2.2_THP_的利弊与关闭_THPPitfalls/index.md)
- [3.2.2.3 内存压缩、回收与 kswapd 的干扰](03.02.2.3_内存压缩_回收与_kswapd_的干扰_ReclaimInterference/index.md)

---

## 导航

← 上一节：[3.2.1 锁页与预故障化](../03.02.1_锁页与预故障化_LockingAndPrefaulting/index.md)
↑ 返回上级：[3.2 内存管理与页面行为](../index.md)
下一节：[3.2.3 内存映射与共享内存](../03.02.3_内存映射与共享内存_MmapAndSharedMemory/index.md) →
