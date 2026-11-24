# 1.1.3 互斥锁、读写锁与自旋锁 mutex rwlock and spinlock

**介绍**: 深入剖析 `std::mutex` / `std::timed_mutex`、读写锁（`std::shared_mutex` / `pthread_rwlock_t`）与自旋锁（Spinlock）的语义、同步机制、开销成本、适用场景与公平性/饥饿权衡，帮助在传统同步原语与低延迟无锁方案之间做出稳健的工程决策。

## 小节索引

- [1.1.3.1 互斥锁（Mutex）：独占语义与内核阻塞代价](./1.1.3.1_互斥锁（Mutex）：独占语义与内核阻塞代价/index.md)
- [1.1.3.2 读写锁（Read-Write Lock）：共享读与独占写](./1.1.3.2_读写锁（Read-Write%20Lock）：共享读与独占写/index.md)
- [1.1.3.3 自旋锁（Spinlock）：忙等循环与适用边界](./1.1.3.3_自旋锁（Spinlock）：忙等循环与适用边界/index.md)
- [1.1.3.4 公平性、饥饿与锁/无锁演进对比](./1.1.3.4_公平性、饥饿与锁%20无锁演进对比/index.md)
- [1.1.3.5 可运行 C++ 示例：`std::mutex`、`std::shared_mutex` 与自旋锁对比](./1.1.3.5_可运行%20C++%20示例：`std%20mutex`、`std%20shared_mutex`%20与自旋锁对比/index.md)

## 导航

* 上一节: [1.1.2 数据竞争、竞态条件与线程安全 data race race condition and thread safety](../1.1.2_数据竞争、竞态条件与线程安全_data_race_race_condition_and_thread_safety/index.md)
* 返回上级: [1.1 并发基础与同步原语  concurrency fundamentals](../index.md)
* 下一节: [1.1.4 条件变量、信号量与屏障  condition variable semaphore and barrier](../1.1.4_条件变量、信号量与屏障_condition_variable_semaphore_and_barrier/index.md)
