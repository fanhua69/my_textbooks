# 02 通用块层、I/O 调度器、NVMe 多队列（blk-mq）与 DMA 传输

**介绍**: 理解请求合并/分发、硬件队列与 CPU 核映射以及存储控制器通过 DMA 完成数据搬运的流程。

---

## 导航

← 上一节：[5.1.1 文件描述符、打开文件表、Inode / Dentry 缓存与路径解析开销](../01_fd_inode_dentry_缓存与路径解析开销/index.md)
↑ 返回上级：[5.1 虚拟文件系统（VFS）、元数据与块设备 I/O 栈](../index.md)
下一节：[5.2 页缓存（Page Cache）、脏页回写与 Direct I/O](../../02_页缓存_脏页回写与_direct_i_o/index.md) →
