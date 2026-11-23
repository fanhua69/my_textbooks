# 1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms

从线程暂停、调度依赖和系统整体进度角度理解阻塞与非阻塞。

---

## 小节索引

- [1.3.1.1 根本问题与 Blocking 算法：当线程被暂停时，其他线程还能继续吗？](./1.3.1.1_根本问题与%20Blocking%20算法：当线程被暂停时，其他线程还能继续吗？/index.md)
- [1.3.1.2 Non-blocking 算法与“线程暂停”的本质区别](./1.3.1.2_Non-blocking%20算法与“线程暂停”的本质区别/index.md)
- [1.3.1.3 三种 Non-blocking Progress Guarantees（进度保证）概览](./1.3.1.3_三种%20Non-blocking%20Progress%20Guarantees（进度保证）概览/index.md)
- [1.3.1.4 C++ 标准库视角与低延迟系统中的现实工程考量](./1.3.1.4_C++%20标准库视角与低延迟系统中的现实工程考量/index.md)
- [1.3.1.5 可运行 C++ 示例：无锁原子累加推进与调度停顿隔离演示](./1.3.1.5_可运行%20C++%20示例：无锁原子累加推进与调度停顿隔离演示/index.md)

## 导航

← 上一节：[1.2 并发拓扑与生产者消费者模型  concurrency topologies](../../1.2_并发拓扑与生产者消费者模型_concurrency_topologies/index.md)
↑ 返回上级：[1.3 Lock-Free、Wait-Free 与进度保证  progress guarantees](../index.md)
下一节：[1.3.2 Obstruction-Free：无障碍  obstruction free](../1.3.2_Obstruction-Free：无障碍_obstruction_free/index.md) →
