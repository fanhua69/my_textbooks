# 3.1.2.2 mlock / mlockall / MAP POPULATE 与 VirtualLock 实践

在启动阶段完成物理页 fault 与锁定，防止运行期热路径触发缺页或被换出。

---

## 导航

← 上一节：[3.1.2.1 缺页类型分类、写时复制（COW）与透明大页（THP）抖动](../01_缺页类型分类_写时复制_cow_与透明大页_thp_抖动/index.md)
↑ 返回上级：[3.1.2 Minor/Major Page Fault、写时复制（COW）与热路径防缺页](../index.md)
下一节：[3.1.3 mmap / munmap / madvise 与 Windows VirtualAlloc / VirtualProtect 对比](../../03_mmap_madvise_与_virtualalloc_语义对比/index.md) →
