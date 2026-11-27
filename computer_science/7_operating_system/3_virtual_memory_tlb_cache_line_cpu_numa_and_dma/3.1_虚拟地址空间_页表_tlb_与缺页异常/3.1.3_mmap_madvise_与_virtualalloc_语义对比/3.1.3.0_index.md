# 3.1.3 mmap / munmap / madvise 与 Windows VirtualAlloc / VirtualProtect 对比

**介绍**: 对比匿名映射、文件映射、保护属性修改与内存建议标志在三平台下的实现与副作用。

## 目录

- [3.1.3.1 POSIX mmap / munmap / madvise（MADV DONTNEED / MADV HUGEPAGE）](3.1.3.1_posix_mmap_munmap_madvise_语义与副作用/index.md)
- [3.1.3.2 Windows VirtualAlloc / VirtualFree / VirtualProtect 内存管理](3.1.3.2_windows_virtualalloc_virtualfree_virtualprotect_管理/index.md)

## 导航

← 上一节：[3.1.2 Minor/Major Page Fault、写时复制（COW）与热路径防缺页](../3.1.2_page_fault_cow_与热路径防缺页策略/index.md)
↑ 返回上级：[3.1 虚拟地址空间、页表、TLB 与缺页异常（Page Fault）](../index.md)
下一节：[3.2 CPU 架构、Cache Line 层次与缓存一致性协议](../../3.2_cpu_架构_cache_line_层次与缓存一致性协议/index.md) →
