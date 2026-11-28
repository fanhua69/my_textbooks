# 5 文件系统、存储 I/O 栈与持久化性能

**介绍**: 从 VFS 与块设备层剖析文件系统结构、页缓存与脏页回写、同步/异步/直接 I/O（Direct I/O）与 NVMe/持久化路径，理解存储 I/O 对系统延迟与稳定性的影响。


## 目录

- [5.1 虚拟文件系统（VFS）、元数据与块设备 I/O 栈](5.1_index.md)
- [5.2 页缓存（Page Cache）、脏页回写与 Direct I/O](5.2_index.md)
- [5.3 主流文件系统特性与持久化语义（fsync / F FULLFSYNC / Flush）](5.3_index.md)

---

## 导航

⬅️ 上一节：[4 进程间通信（IPC）、共享内存与高速数据通道](4_index.md)
⏺️ 当前节：[5 文件系统、存储 I/O 栈与持久化性能](5_index.md)
➡️ 下一节：[6 任务调度、CPU Binding 与尾延迟（P99 / P99.9）治理](6_index.md)
⬆️ 返回上级：[7 Operating Systems Engineering: Low-Latency & Systems Architecture (Linux, macOS & Windows)](contents.md)
