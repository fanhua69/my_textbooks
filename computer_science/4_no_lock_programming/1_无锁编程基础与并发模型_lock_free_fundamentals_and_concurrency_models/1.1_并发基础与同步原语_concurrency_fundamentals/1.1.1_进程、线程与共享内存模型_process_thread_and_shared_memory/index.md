# 1.1.1 进程、线程与共享内存模型 process thread and shared memory

**介绍**: 深入理解进程隔离边界、线程执行上下文、共享地址空间与内存模型、线程局部存储（TLS）、线程间通信与同步协作，以及跨系统与锁/无锁设计的工程取舍，为后续学习内存序（`std::memory_order`）、原子操作与无锁数据结构打下扎实基础。

## 小节索引

- [1.1.1.1 进程与线程：隔离边界 vs 共享执行流](./1.1.1.1_进程与线程：隔离边界%20vs%20共享执行流/index.md)
- [1.1.1.2 共享内存模型与无锁编程的起点](./1.1.1.2_共享内存模型与无锁编程的起点/index.md)
- [1.1.1.3 线程局部存储（TLS：Thread-Local Storage）](./1.1.1.3_线程局部存储（TLS：Thread-Local%20Storage）/index.md)
- [1.1.1.4 线程间通信（Thread Communication）](./1.1.1.4_线程间通信（Thread%20Communication）/index.md)
- [1.1.1.5 历史演进、系统差异与工程对比](./1.1.1.5_历史演进、系统差异与工程对比/index.md)
- [1.1.1.6 可运行 C++ 示例：共享地址空间、TLS 与同步协作对比](./1.1.1.6_可运行%20C++%20示例：共享地址空间、TLS%20与同步协作对比/index.md)

---

## 目录

- [1.1.1.1 进程与线程：隔离边界 vs 共享执行流](1.1.1.1_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%EF%BC%9A%E9%9A%94%E7%A6%BB%E8%BE%B9%E7%95%8C%20vs%20%E5%85%B1%E4%BA%AB%E6%89%A7%E8%A1%8C%E6%B5%81/index.md)
- [1.1.1.2 共享内存模型与无锁编程的起点](1.1.1.2_共享内存模型与无锁编程的起点/index.md)
- [1.1.1.3 线程局部存储（TLS：Thread-Local Storage）](1.1.1.3_%E7%BA%BF%E7%A8%8B%E5%B1%80%E9%83%A8%E5%AD%98%E5%82%A8%EF%BC%88TLS%EF%BC%9AThread-Local%20Storage%EF%BC%89/index.md)
- [1.1.1.4 线程间通信（Thread Communication）](1.1.1.4_%E7%BA%BF%E7%A8%8B%E9%97%B4%E9%80%9A%E4%BF%A1%EF%BC%88Thread%20Communication%EF%BC%89/index.md)
- [1.1.1.5 历史演进、系统差异与工程对比](1.1.1.5_历史演进、系统差异与工程对比/index.md)
- [1.1.1.6 可运行 C++ 示例：共享地址空间、TLS 与同步协作对比](1.1.1.6_%E5%8F%AF%E8%BF%90%E8%A1%8C%20C%2B%2B%20%E7%A4%BA%E4%BE%8B%EF%BC%9A%E5%85%B1%E4%BA%AB%E5%9C%B0%E5%9D%80%E7%A9%BA%E9%97%B4%E3%80%81TLS%20%E4%B8%8E%E5%90%8C%E6%AD%A5%E5%8D%8F%E4%BD%9C%E5%AF%B9%E6%AF%94/index.md)

## 导航

- **上一层**：[1.1 并发基础与同步原语  concurrency fundamentals](../index.md)
- **前一节**：[4 No-Lock Programming：C++ 无锁编程](../../../index.md)
- **后一节**：[1.1.2 数据竞争、竞态条件与线程安全 data race race condition and thread safety](../1.1.2_数据竞争、竞态条件与线程安全_data_race_race_condition_and_thread_safety/index.md)
