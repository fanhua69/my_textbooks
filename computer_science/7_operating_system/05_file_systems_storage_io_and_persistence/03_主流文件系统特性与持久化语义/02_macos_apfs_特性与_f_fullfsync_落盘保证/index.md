# 02 macOS APFS（克隆/快照/空间共享）与 F FULLFSYNC 落盘保证

**介绍**: 掌握 APFS 写时复制克隆/快照机制，以及 macOS 上 fsync 与 F_FULLFSYNC 在驱动/设备缓存刷盘上的差异。

---

## 导航

← 上一节：[5.3.1 Linux 文件系统（ext4 / XFS）与 fsync / fdatasync 持久化语义](../01_linux_文件系统与_fsync_fdatasync_语义/index.md)
↑ 返回上级：[5.3 主流文件系统特性与持久化语义（fsync / F FULLFSYNC / Flush）](../index.md)
下一节：[5.3.3 Windows NTFS / ReFS 与 FlushFileBuffers / WriteFile 异步刷盘](../03_windows_ntfs_refs_与持久化刷盘机制/index.md) →
