# 1.1.4 条件变量、信号量与屏障 condition variable semaphore and barrier

掌握阻塞式协调原语（条件变量 `std::condition_variable`、计数信号量 `std::counting_semaphore` / `std::binary_semaphore` 与线程屏障 `std::barrier` / `std::latch`）的工作语义、虚假唤醒与丢失唤醒防治、系统差异，以及它们与原子操作（`std::atomic` / C++20 `atomic::wait`/`notify`）的协作与取舍关系。

## 小节索引

- [1.1.4.1 条件变量（Condition Variable）：谓词等待与唤醒机制](./1.1.4.1_条件变量（Condition%20Variable）：谓词等待与唤醒机制/index.md)
- [1.1.4.2 信号量（Semaphore）：许可计数与资源并发控制](./1.1.4.2_信号量（Semaphore）：许可计数与资源并发控制/index.md)
- [1.1.4.3 屏障（Latch 与 Barrier）：阶段同步与多线程会合](./1.1.4.3_屏障（Latch%20与%20Barrier）：阶段同步与多线程会合/index.md)
- [1.1.4.4 与原子操作的协作关系：阻塞原语 vs. `std::atomic::wait`](./1.1.4.4_与原子操作的协作关系：阻塞原语%20vs.%20`std%20atomic%20wait`/index.md)
- [1.1.4.5 可运行 C++ 示例：`std::condition_variable` 与 `std::latch` 协作](./1.1.4.5_可运行%20C++%20示例：`std%20condition_variable`%20与%20`std%20latch`%20协作/index.md)

## 导航

← 上一节：[1.1.3 互斥锁、读写锁与自旋锁  mutex rwlock and spinlock](../1.1.3_互斥锁、读写锁与自旋锁_mutex_rwlock_and_spinlock/index.md)
↑ 返回上级：[1.1 并发基础与同步原语  concurrency fundamentals](../index.md)
下一节：[1.1.5 锁竞争、上下文切换与优先级反转  lock contention context switch and priority inversion](../1.1.5_锁竞争、上下文切换与优先级反转_lock_contention_context_switch_and_priority_inversion/index.md) →
