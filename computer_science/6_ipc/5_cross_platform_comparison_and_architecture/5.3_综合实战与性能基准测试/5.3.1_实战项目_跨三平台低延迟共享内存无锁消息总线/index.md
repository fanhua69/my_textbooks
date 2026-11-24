# 5.3.1 实战项目：跨三平台低延迟共享内存无锁消息总线

**介绍**: 实现支持 Linux（memfd + futex）、macOS（xpc_shmem/shm + ulock）与 Windows（FileMapping + WaitOnAddress）的统一总线。

---

## 导航

← 上一节：[5.2 跨平台 C++ IPC 抽象层与混合架构设计](../../5.2_跨平台_c__ipc_抽象层与混合架构设计/index.md)
↑ 返回上级：[5.3 综合实战与性能基准测试](../index.md)
下一节：[5.3.2 IPC 延迟与吞吐基准测试（Round-Trip Latency & Tail Latency）](../5.3.2_ipc_延迟与吞吐基准测试_round_trip_latency_tail_latency/index.md) →
