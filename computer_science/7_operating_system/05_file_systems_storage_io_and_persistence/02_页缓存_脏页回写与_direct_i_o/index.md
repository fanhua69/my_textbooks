# 02 页缓存（Page Cache）、脏页回写与 Direct I/O

**介绍**: 掌握读缓存、后台刷盘抖动治理以及绕过页缓存的 Direct I/O 适用场景与对齐要求。

## 目录

- [01 Page Cache 读命中、预读（Read-ahead）与脏页（Dirty Page）后台回写抖动](01_page_cache_预读与脏页回写延迟毛刺/index.md)
- [02 Buffered I/O vs Direct I/O（O DIRECT / FILE FLAG NO BUFFERING）与对齐约束](02_buffered_io_vs_direct_io_与对齐约束/index.md)

## 导航

← 上一节：[5.1 虚拟文件系统（VFS）、元数据与块设备 I/O 栈](../01_vfs_元数据与块设备_i_o_栈/index.md)
↑ 返回上级：[5 文件系统、存储 I/O 栈与持久化性能](../index.md)
下一节：[5.3 主流文件系统特性与持久化语义（fsync / F FULLFSYNC / Flush）](../03_主流文件系统特性与持久化语义/index.md) →
