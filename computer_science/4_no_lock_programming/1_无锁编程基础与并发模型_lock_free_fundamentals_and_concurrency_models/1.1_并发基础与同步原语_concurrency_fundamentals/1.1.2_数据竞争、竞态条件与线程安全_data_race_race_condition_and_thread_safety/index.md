# 1.1.2 数据竞争、竞态条件与线程安全 data race race condition and thread safety

**介绍**: 深入区分 **Data Race（数据竞争）**、**Race Condition（竞态条件）**、**Thread Safety（线程安全）** 与 **Reentrant（可重入性）**，彻底理解 C++ 内存模型下数据竞争为何属于**未定义行为（Undefined Behavior, UB）**，并掌握排查、消除竞态与编写可靠并发代码的工程准则。

## 小节索引

- [1.1.2.1 核心概念辨析：Data Race vs. Race Condition](./1.1.2.1_核心概念辨析：Data%20Race%20vs.%20Race%20Condition/index.md)
- [1.1.2.2 为什么 C++ 中的 Data Race 是未定义行为（UB）？](./1.1.2.2_为什么%20C++%20中的%20Data%20Race%20是未定义行为（UB）？/index.md)
- [1.1.2.3 线程安全与可重入性的工程边界](./1.1.2.3_线程安全与可重入性的工程边界/index.md)
- [1.1.2.4 历史演进、系统差异与工程对比](./1.1.2.4_历史演进、系统差异与工程对比/index.md)
- [1.1.2.5 可运行 C++ 示例：Data Race 与 Race Condition 对比演示](./1.1.2.5_可运行%20C++%20示例：Data%20Race%20与%20Race%20Condition%20对比演示/index.md)

## 导航

← 上一节：[1.1.1 进程、线程与共享内存模型  process thread and shared memory](../1.1.1_进程、线程与共享内存模型_process_thread_and_shared_memory/index.md)
↑ 返回上级：[1.1 并发基础与同步原语  concurrency fundamentals](../index.md)
下一节：[1.1.3 互斥锁、读写锁与自旋锁  mutex rwlock and spinlock](../1.1.3_互斥锁、读写锁与自旋锁_mutex_rwlock_and_spinlock/index.md) →
