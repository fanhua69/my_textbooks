# 1.1.3.1 互斥锁（Mutex）：独占语义与内核阻塞代价

**介绍**: > **简介**：互斥锁（Mutual Exclusion Lock）是最基础的独占同步原语：在任一时刻，最多只允许一个线程持有锁并进入临界区（Critical Section），其他尝试获取同一把锁的线程将被阻塞（在现代操作系统中通常通过用户态快速路径 + 内核态等待队列挂起/唤醒实现）。

---

互斥锁（Mutual Exclusion Lock）是最基础的独占同步原语：在任一时刻，最多只允许一个线程持有锁并进入临界区（Critical Section），其他尝试获取同一把锁的线程将被阻塞（在现代操作系统中通常通过用户态快速路径 + 内核态等待队列挂起/唤醒实现）。

### 核心语义与 C++ 标准原语

* **排他所有权（Exclusive Ownership）**：同一时刻只能有一个线程拥有锁；持锁线程释放锁之前，其他线程无法进入受保护的临界区。
* **同步关系（Synchronizes-With）**：线程 A 释放锁（`unlock()`）与随后线程 B 获取同一把锁（`lock()`）之间构成 `synchronizes-with` 关系，从而建立 `happens-before` 顺序，保证线程 A 在临界区内的写入对线程 B 可见，且不会产生数据竞争。
* **C++ 标准库组件**：
* `std::mutex`：基础独占互斥锁，提供 `lock()`、`try_lock()`、`unlock()`。
* `std::timed_mutex` / `std::recursive_timed_mutex`：支持 `try_lock_for()` 与 `try_lock_until()` 超时获取，适合避免无限期等待的场景。
* `std::recursive_mutex`：允许同一线程多次重入加锁（需配对解锁），但过度依赖递归锁往往掩盖了所有权或锁粒度设计问题。
* RAII 守卫（`std::lock_guard`、`std::unique_lock`、`std::scoped_lock`）：通过作用域析构自动解锁，降低异常或提前返回导致的死锁风险；`std::scoped_lock` 可同时锁定多把互斥锁并采用死锁避免算法。



### 成本与工程注意点

* **争用下的阻塞与上下文切换**：无争用时，现代互斥锁可在用户态通过原子操作快速完成加锁/解锁；一旦发生争用，等待线程可能陷入内核态休眠，带来线程切换、缓存局部性下降以及调度延迟抖动。
* **持锁时间与临界区范围**：临界区内应避免执行磁盘/网络 I/O、复杂分配或未知外部回调，否则会放大锁争用与尾延迟。


---

## 导航

- **上一层**：[1.1.3 互斥锁、读写锁与自旋锁 mutex rwlock and spinlock](../index.md)
- **前一节**：[1.1.2 数据竞争、竞态条件与线程安全 data race race condition and thread safety](../../1.1.2_数据竞争、竞态条件与线程安全_data_race_race_condition_and_thread_safety/index.md)
- **后一节**：[1.1.3.2 读写锁（Read-Write Lock）：共享读与独占写](../1.1.3.2_%E8%AF%BB%E5%86%99%E9%94%81%EF%BC%88Read-Write%20Lock%EF%BC%89%EF%BC%9A%E5%85%B1%E4%BA%AB%E8%AF%BB%E4%B8%8E%E7%8B%AC%E5%8D%A0%E5%86%99/index.md)
