# 6 任务调度、CPU Binding 与尾延迟（P99 / P99.9）治理

深入多核调度器算法、CPU Binding（绑核与核隔离）、上下文切换与中断/软中断干扰、同步/无锁原语与优先级反转，构建面向 P99/P99.9/P99.99 尾延迟的系统级调度工程体系。

## 本节目录

- [6.1 多核任务调度器核心机制与切换开销](01_多核任务调度器核心机制与切换开销/index.md)
- [6.2 CPU Binding（绑核）、核隔离与三大平台调度器对比](02_cpu_binding_核隔离与三大平台调度器对比/index.md)
- [6.3 并发同步、优先级反转与尾延迟（P99 / P99.9 / P99.99）治理](03_并发同步_优先级反转与尾延迟治理/index.md)

---

## 导航

← 上一节：[5 文件系统、存储 I/O 栈与持久化性能](../05_file_systems_storage_io_and_persistence/index.md)
↑ 返回上级：[Operating Systems Engineering: Low-Latency & Systems Architecture (Linux, macOS & Windows)](../index.md)
下一节：[7 操作系统安全模型、苹果安全机制与 IPC 通信边界](../07_os_security_apple_security_and_ipc_boundaries/index.md) →
