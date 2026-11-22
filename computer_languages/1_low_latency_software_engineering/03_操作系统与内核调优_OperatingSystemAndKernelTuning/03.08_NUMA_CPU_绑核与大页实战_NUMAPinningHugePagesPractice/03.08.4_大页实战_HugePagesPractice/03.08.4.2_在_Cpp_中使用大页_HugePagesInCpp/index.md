# 3.8.4.2 在 C++ 中使用大页

让分配器与数据结构落在大页上。

## 本节目录

- [3.8.4.2.1 mmap 的 MAP_HUGETLB 与 memfd 大页](03.08.4.2.1_mmap_的_MAP_HUGETLB_与_memfd_大页_MmapHugetlbMemfd/index.md)
- [3.8.4.2.2 自定义分配器与 arena 放置到大页](03.08.4.2.2_自定义分配器与_arena_放置到大页_AllocatorOnHugePages/index.md)
- [3.8.4.2.3 二进制代码段大页](03.08.4.2.3_二进制代码段大页_CodeSegmentHugePages/index.md)

---

## 导航

← 上一节：[3.8.4.1 大页预留与挂载](../03.08.4.1_大页预留与挂载_HugePageReservation/index.md)
↑ 返回上级：[3.8.4 大页（Huge Pages）实战](../index.md)
下一节：[3.8.4.3 THP 管理与验证](../03.08.4.3_THP_管理与验证_THPManagementVerification/index.md) →
