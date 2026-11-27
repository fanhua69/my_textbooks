# 1.1.4 条件变量、信号量与屏障 condition variable semaphore and barrier

**介绍**: 掌握阻塞式协调原语（条件变量 `std::condition_variable`、计数信号量 `std::counting_semaphore` / `std::binary_semaphore` 与线程屏障 `std::barrier` / `std::latch`）的工作语义、虚假唤醒与丢失唤醒防治、系统差异，以及它们与原子操作（`std::atomic` / C++20 `atomic::wait`/`notify`）的协作与取舍关系。

## 小节索引

- [1.1.4.1 条件变量（Condition Variable）：谓词等待与唤醒机制](./1.1.4.1_条件变量（Condition%20Variable）：谓词等待与唤醒机制/index.md)
- [1.1.4.2 信号量（Semaphore）：许可计数与资源并发控制](./1.1.4.2_信号量（Semaphore）：许可计数与资源并发控制/index.md)
- [1.1.4.3 屏障（Latch 与 Barrier）：阶段同步与多线程会合](./1.1.4.3_屏障（Latch%20与%20Barrier）：阶段同步与多线程会合/index.md)
- [1.1.4.4 与原子操作的协作关系：阻塞原语 vs. `std::atomic::wait`](./1.1.4.4_与原子操作的协作关系：阻塞原语%20vs.%20`std%20atomic%20wait`/index.md)
- [1.1.4.5 可运行 C++ 示例：`std::condition_variable` 与 `std::latch` 协作](./1.1.4.5_可运行%20C++%20示例：`std%20condition_variable`%20与%20`std%20latch`%20协作/index.md)

---

## 目录

- [1.1.4.1 条件变量（Condition Variable）：谓词等待与唤醒机制](1.1.4.1_%E6%9D%A1%E4%BB%B6%E5%8F%98%E9%87%8F%EF%BC%88Condition%20Variable%EF%BC%89%EF%BC%9A%E8%B0%93%E8%AF%8D%E7%AD%89%E5%BE%85%E4%B8%8E%E5%94%A4%E9%86%92%E6%9C%BA%E5%88%B6/index.md)
- [1.1.4.2 信号量（Semaphore）：许可计数与资源并发控制](1.1.4.2_信号量（Semaphore）：许可计数与资源并发控制/index.md)
- [1.1.4.3 屏障（Latch 与 Barrier）：阶段同步与多线程会合](1.1.4.3_%E5%B1%8F%E9%9A%9C%EF%BC%88Latch%20%E4%B8%8E%20Barrier%EF%BC%89%EF%BC%9A%E9%98%B6%E6%AE%B5%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E4%BC%9A%E5%90%88/index.md)
- [1.1.4.4 与原子操作的协作关系：阻塞原语 vs. `std::atomic::wait`](1.1.4.4_%E4%B8%8E%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C%E7%9A%84%E5%8D%8F%E4%BD%9C%E5%85%B3%E7%B3%BB%EF%BC%9A%E9%98%BB%E5%A1%9E%E5%8E%9F%E8%AF%AD%20vs.%20%60std%20atomic%20wait%60/index.md)
- [1.1.4.5 可运行 C++ 示例：`std::condition_variable` 与 `std::latch` 协作](1.1.4.5_%E5%8F%AF%E8%BF%90%E8%A1%8C%20C%2B%2B%20%E7%A4%BA%E4%BE%8B%EF%BC%9A%60std%20condition_variable%60%20%E4%B8%8E%20%60std%20latch%60%20%E5%8D%8F%E4%BD%9C/index.md)

## 导航

← 上一节：[1.1.3 互斥锁、读写锁与自旋锁 mutex rwlock and spinlock](../1.1.3_互斥锁、读写锁与自旋锁_mutex_rwlock_and_spinlock/index.md)
↑ 返回上级：[1.1 并发基础与同步原语  concurrency fundamentals](../index.md)
下一节：[1.1.5 锁竞争、上下文切换与优先级反转  lock contention context switch and priority inversion](../1.1.5_锁竞争、上下文切换与优先级反转_lock_contention_context_switch_and_priority_inversion/index.md) →
