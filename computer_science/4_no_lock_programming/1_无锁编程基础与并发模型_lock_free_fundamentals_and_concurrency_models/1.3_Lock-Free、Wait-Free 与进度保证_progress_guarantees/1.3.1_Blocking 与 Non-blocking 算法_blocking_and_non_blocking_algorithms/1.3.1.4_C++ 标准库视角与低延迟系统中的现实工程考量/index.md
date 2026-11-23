# 1.3.1.4 C++ 标准库视角与低延迟系统中的现实工程考量

> **简介**：C++11 引入了 `<atomic>`，C++20 提供了 `std::atomic<T>::is_always_lock_free`（编译期常量），运行时也可通过 `obj.is_lock_free()` 检查特定原子对象是否由无锁硬件指令实现。

---

## 原子操作层级 vs. 算法层级

C++11 引入了 `<atomic>`，C++20 提供了 `std::atomic<T>::is_always_lock_free`（编译期常量），运行时也可通过 `obj.is_lock_free()` 检查特定原子对象是否由无锁硬件指令实现。

但工程上必须严格区分两个层次：
1. **底层原子操作的进度保证**（例如硬件 `CMPXCHG` / `LDXR+STXR` 是否无锁）；
2. **由多步原子操作组成的上层数据结构/算法的进度保证**（例如队列、栈、链表、内存回收机制）。

底层原子指令具备无锁属性，**并不自动意味着**由它拼出来的上层并发算法就是 Lock-Free 或 Wait-Free。

## 为什么低延迟与交易系统关注 Non-blocking？又为何不能盲目迷信？

在高频行情处理、订单撮合、风控与路由等低延迟系统中，线程若通过阻塞锁共享队列，一旦某个线程持锁延迟或被换出，其他关键路径线程的 **Tail Latency（尾延迟：P99、P99.9、Max）** 就会被放大。

但也要清醒认识：**Non-blocking / Lock-Free 不等于绝对更低延迟**。无锁算法在工程上仍面临：
- **CAS Retry（冲突重试）**与高争用下的循环开销；
- **Cache Line Contention（缓存行竞争）**、**Cache Miss（缓存未命中）**与 **False Sharing（伪共享）**；
- **Memory Reclamation（安全内存回收，如 Hazard Pointer / RCU / 纪元回收）**带来的额外复杂度与开销。

因此，在真实系统里，既要理解进度保证的理论边界，也要实测 **P50、P99、P99.9 与最大延迟**，用数据做决策。

---


---

## 导航

- **上一层**：[1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms](../index.md)
- **前一节**：[1.3.1.3 三种 Non-blocking Progress Guarantees（进度保证）概览](../1.3.1.3_%E4%B8%89%E7%A7%8D%20Non-blocking%20Progress%20Guarantees%EF%BC%88%E8%BF%9B%E5%BA%A6%E4%BF%9D%E8%AF%81%EF%BC%89%E6%A6%82%E8%A7%88/index.md)
- **后一节**：[1.3.1.5 可运行 C++ 示例：无锁原子累加推进与调度停顿隔离演示](../1.3.1.5_%E5%8F%AF%E8%BF%90%E8%A1%8C%20C%2B%2B%20%E7%A4%BA%E4%BE%8B%EF%BC%9A%E6%97%A0%E9%94%81%E5%8E%9F%E5%AD%90%E7%B4%AF%E5%8A%A0%E6%8E%A8%E8%BF%9B%E4%B8%8E%E8%B0%83%E5%BA%A6%E5%81%9C%E9%A1%BF%E9%9A%94%E7%A6%BB%E6%BC%94%E7%A4%BA/index.md)
