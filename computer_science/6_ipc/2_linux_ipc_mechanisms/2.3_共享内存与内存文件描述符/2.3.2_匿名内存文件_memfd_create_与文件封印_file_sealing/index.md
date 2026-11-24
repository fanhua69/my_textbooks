# 2.3.2 匿名内存文件 memfd create 与文件封印（File Sealing）

**介绍**: 使用 memfd 避免命名冲突，并通过 F_SEAL_SHRINK / F_SEAL_WRITE 防止对端恶意截断引发 SIGBUS。

---

## 导航

← 上一节：[2.3.1 POSIX 共享内存（shm open + mmap）与 System V shm 对比](../2.3.1_posix_共享内存_shm_open_mmap_与_system_v_shm_对比/index.md)
↑ 返回上级：[2.3 共享内存与内存文件描述符](../index.md)
下一节：[2.3.3 大页内存（HugeTLB / THP）与 NUMA 亲和性优化](../2.3.3_大页内存_hugetlb_thp_与_numa_亲和性优化/index.md) →
