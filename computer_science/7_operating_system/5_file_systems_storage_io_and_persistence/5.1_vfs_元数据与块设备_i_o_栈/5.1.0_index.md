# 5.1 虚拟文件系统（VFS）、元数据与块设备 I/O 栈

**介绍**: 理解文件抽象、目录/inode 缓存（dentry/inode cache）、块层调度与存储协议栈。

## 目录

- [5.1.1 文件描述符、打开文件表、Inode / Dentry 缓存与路径解析开销](5.1.1_fd_inode_dentry_缓存与路径解析开销/index.md)
- [5.1.2 通用块层、I/O 调度器、NVMe 多队列（blk-mq）与 DMA 传输](5.1.2_块层_blk_mq_nvme_与_dma_传输路径/index.md)

## 导航

← 上一节：[4 进程间通信（IPC）、共享内存与高速数据通道](../../4_ipc_shared_memory_and_data_channels/index.md)
↑ 返回上级：[5 文件系统、存储 I/O 栈与持久化性能](../index.md)
下一节：[5.2 页缓存（Page Cache）、脏页回写与 Direct I/O](../5.2_页缓存_脏页回写与_direct_i_o/index.md) →
