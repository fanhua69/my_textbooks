# 1.3.1.1 根本问题与 Blocking 算法：当线程被暂停时，其他线程还能继续吗？

> **简介**：这一节非常重要，因为它是理解后面三个核心进度保证（Obstruction-Free、Lock-Free、Wait-Free）的基础。我们先不急着陷入复杂数据结构，而是从一个根本问题开始：

---

这一节非常重要，因为它是理解后面三个核心进度保证（Obstruction-Free、Lock-Free、Wait-Free）的基础。我们先不急着陷入复杂数据结构，而是从一个根本问题开始：

> **当多个线程同时执行一个并发算法时，如果某个线程被操作系统暂停（抢占、缺页中断、I/O 等待或挂起）了，其他线程还能不能继续完成工作？**

## 什么是 Blocking 算法？

**Blocking Algorithm（阻塞算法）**是指：一个线程可能因为等待其他线程释放某种资源或满足某个条件，而被迫暂停执行、无法继续完成当前操作。最典型的例子就是互斥锁（`std::mutex`）。

假设有两个线程争用同一把 `std::mutex`：
1. **Thread A** 获得互斥锁并进入临界区（Critical Section）；
2. **Thread A** 恰好在临界区内被操作系统调度器暂停（Preempted）；
3. **Thread B** 尝试获取同一把互斥锁，发现锁已被占用，只能阻塞等待。

## 核心问题：进度依赖（Progress Dependency）与无界等待

在上面的过程中，**Thread B 能否继续完成自己的操作，取决于 Thread A 什么时候恢复运行并释放锁**——这就是 **Progress Dependency（进度依赖）**。

更糟糕的是，普通的 `std::mutex` 不会自动保证持锁线程及时恢复运行。如果 Thread A：
- 被操作系统长时间暂停或调度延迟；
- 发生缺页中断（Page Fault）或陷入长 I/O；
- 发生死锁（Deadlock）；
- 或因异常/逻辑错误迟迟不释放锁；

那么 Thread B 就会陷入长时间等待甚至无限期等待（Unbounded Waiting）。

## Blocking 的主要风险与系统级病理

| 问题 / 现象 | 核心解释 |
| :--- | :--- |
| **Deadlock（死锁）** | 多个线程循环互相等待对方持有的资源，全部无法继续推进 |
| **Priority Inversion（优先级反转）** | 低优先级线程持锁，高优先级线程阻塞等待，若中优先级线程抢占低优先级线程，高优先级任务会被间接无限延迟（在实时与低延迟系统中尤为危险） |
| **Convoying / 护航效应** | 某个线程持锁时间过长或持锁期间被换出，后续线程排队阻塞，多核并行退化为串行甚至停顿，唤醒时还可能引发缓存失效与抢锁抖动 |
| **Scheduler Dependency（调度依赖）** | 算法的整体或局部进度强依赖特定线程获得调度器时间片 |
| **Unbounded Waiting（无界等待）** | 线程等待时长缺乏理论上限，极端情况下可能永远无法返回 |

---


---

## 导航

- **上一层**：[1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms](../index.md)
- **前一节**：[1.2 并发拓扑与生产者消费者模型  concurrency topologies](../../../1.2_并发拓扑与生产者消费者模型_concurrency_topologies/index.md)
- **后一节**：[1.3.1.2 Non-blocking 算法与“线程暂停”的本质区别](../1.3.1.2_Non-blocking%20%E7%AE%97%E6%B3%95%E4%B8%8E%E2%80%9C%E7%BA%BF%E7%A8%8B%E6%9A%82%E5%81%9C%E2%80%9D%E7%9A%84%E6%9C%AC%E8%B4%A8%E5%8C%BA%E5%88%AB/index.md)
