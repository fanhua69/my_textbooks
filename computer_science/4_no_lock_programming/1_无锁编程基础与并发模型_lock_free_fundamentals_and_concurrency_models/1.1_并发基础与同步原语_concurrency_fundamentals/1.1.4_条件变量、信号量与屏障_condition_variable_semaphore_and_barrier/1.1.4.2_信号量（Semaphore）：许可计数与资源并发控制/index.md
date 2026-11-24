# 1.1.4.2 信号量（Semaphore）：许可计数与资源并发控制

**介绍**: > **简介**：信号量维护一个非负整数计数器（表示可用“许可/槽位”的数量）：

---

**信号量**维护一个非负整数计数器（表示可用“许可/槽位”的数量）：

* **`acquire()`（P 操作 / 减计数）**：若计数大于 0，原子递减计数并立即返回；若计数为 0，则阻塞当前线程直到计数变为正数并成功递减。
* **`release(update = 1)`（V 操作 / 加计数）**：原子增加计数（最多不超过模板参数 `LeastMaxValue`），并唤醒正在等待的线程。

## C++20 `std::counting_semaphore` 与 `std::binary_semaphore`

* **计数信号量 vs. 互斥锁**：互斥锁强调“谁加锁、谁解锁”的**所有权**（同一线程加锁与解锁）；信号量侧重**可用许可数量**，线程 A 可以 `acquire()`，线程 B 可以 `release()`，常用于限制并发连接数、缓冲池槽位上限或生产者-消费者计数。
* **二元信号量（`std::binary_semaphore` 即 `std::counting_semaphore<1>`）**：最大计数为 1，但语义上仍与 `std::mutex` 不同——它没有锁所有权概念，且 `release()` 超过上限会触发未定义行为（或取决于实现契约）。
* **与条件变量的对比**：信号量自带计数值，适合“按可用配额放行”；条件变量适合“等待任意复杂谓词成立（如 `count > 0 && !paused`）”，且通常伴随受同一互斥锁保护的结构化数据。


---

## 导航

- **上一层**：[1.1.4 条件变量、信号量与屏障 condition variable semaphore and barrier](../index.md)
- **前一节**：[1.1.4.1 条件变量（Condition Variable）：谓词等待与唤醒机制](../1.1.4.1_%E6%9D%A1%E4%BB%B6%E5%8F%98%E9%87%8F%EF%BC%88Condition%20Variable%EF%BC%89%EF%BC%9A%E8%B0%93%E8%AF%8D%E7%AD%89%E5%BE%85%E4%B8%8E%E5%94%A4%E9%86%92%E6%9C%BA%E5%88%B6/index.md)
- **后一节**：[1.1.4.3 屏障（Latch 与 Barrier）：阶段同步与多线程会合](../1.1.4.3_%E5%B1%8F%E9%9A%9C%EF%BC%88Latch%20%E4%B8%8E%20Barrier%EF%BC%89%EF%BC%9A%E9%98%B6%E6%AE%B5%E5%90%8C%E6%AD%A5%E4%B8%8E%E5%A4%9A%E7%BA%BF%E7%A8%8B%E4%BC%9A%E5%90%88/index.md)
