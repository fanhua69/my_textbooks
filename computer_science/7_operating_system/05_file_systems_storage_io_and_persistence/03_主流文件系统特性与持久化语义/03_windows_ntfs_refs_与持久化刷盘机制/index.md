# 5.3.3 Windows NTFS / ReFS 与 FlushFileBuffers / WriteFile 异步刷盘

理解 NTFS 日志/元文件、文件写入缓存与显式刷盘操作对吞吐和延迟的影响。

---

## 导航

← 上一节：[5.3.2 macOS APFS（克隆/快照/空间共享）与 F FULLFSYNC 落盘保证](../02_macos_apfs_特性与_f_fullfsync_落盘保证/index.md)
↑ 返回上级：[5.3 主流文件系统特性与持久化语义（fsync / F FULLFSYNC / Flush）](../index.md)
下一节：[6 任务调度、CPU Binding 与尾延迟（P99 / P99.9）治理](../../../06_task_scheduling_cpu_binding_and_tail_latency/index.md) →
