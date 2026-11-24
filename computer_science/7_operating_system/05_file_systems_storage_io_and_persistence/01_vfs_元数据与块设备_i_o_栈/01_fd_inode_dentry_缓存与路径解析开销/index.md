# 5.1.1 文件描述符、打开文件表、Inode / Dentry 缓存与路径解析开销

分析频繁 open/stat/lookup 的内核路径开销，以及目录项/索引节点缓存命中率对性能的影响。

---

## 导航

← 上一节：[4 进程间通信（IPC）、共享内存与高速数据通道](../../../04_ipc_shared_memory_and_data_channels/index.md)
↑ 返回上级：[5.1 虚拟文件系统（VFS）、元数据与块设备 I/O 栈](../index.md)
下一节：[5.1.2 通用块层、I/O 调度器、NVMe 多队列（blk-mq）与 DMA 传输](../02_块层_blk_mq_nvme_与_dma_传输路径/index.md) →
