# 1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms

**介绍**: 从线程暂停、调度依赖和系统整体进度角度理解阻塞与非阻塞。

---

## 小节索引

- [1.3.1.1 根本问题与 Blocking 算法：当线程被暂停时，其他线程还能继续吗？](./1.3.1.1_根本问题与%20Blocking%20算法：当线程被暂停时，其他线程还能继续吗？/index.md)
- [1.3.1.2 Non-blocking 算法与“线程暂停”的本质区别](./1.3.1.2_Non-blocking%20算法与“线程暂停”的本质区别/index.md)
- [1.3.1.3 三种 Non-blocking Progress Guarantees（进度保证）概览](./1.3.1.3_三种%20Non-blocking%20Progress%20Guarantees（进度保证）概览/index.md)
- [1.3.1.4 C++ 标准库视角与低延迟系统中的现实工程考量](./1.3.1.4_C++%20标准库视角与低延迟系统中的现实工程考量/index.md)
- [1.3.1.5 可运行 C++ 示例：无锁原子累加推进与调度停顿隔离演示](./1.3.1.5_可运行%20C++%20示例：无锁原子累加推进与调度停顿隔离演示/index.md)

---

## 目录

- [1.3.1.1 根本问题与 Blocking 算法：当线程被暂停时，其他线程还能继续吗？](1.3.1.1_%E6%A0%B9%E6%9C%AC%E9%97%AE%E9%A2%98%E4%B8%8E%20Blocking%20%E7%AE%97%E6%B3%95%EF%BC%9A%E5%BD%93%E7%BA%BF%E7%A8%8B%E8%A2%AB%E6%9A%82%E5%81%9C%E6%97%B6%EF%BC%8C%E5%85%B6%E4%BB%96%E7%BA%BF%E7%A8%8B%E8%BF%98%E8%83%BD%E7%BB%A7%E7%BB%AD%E5%90%97%EF%BC%9F/index.md)
- [1.3.1.2 Non-blocking 算法与“线程暂停”的本质区别](1.3.1.2_Non-blocking%20%E7%AE%97%E6%B3%95%E4%B8%8E%E2%80%9C%E7%BA%BF%E7%A8%8B%E6%9A%82%E5%81%9C%E2%80%9D%E7%9A%84%E6%9C%AC%E8%B4%A8%E5%8C%BA%E5%88%AB/index.md)
- [1.3.1.3 三种 Non-blocking Progress Guarantees（进度保证）概览](1.3.1.3_%E4%B8%89%E7%A7%8D%20Non-blocking%20Progress%20Guarantees%EF%BC%88%E8%BF%9B%E5%BA%A6%E4%BF%9D%E8%AF%81%EF%BC%89%E6%A6%82%E8%A7%88/index.md)
- [1.3.1.4 C++ 标准库视角与低延迟系统中的现实工程考量](1.3.1.4_C%2B%2B%20%E6%A0%87%E5%87%86%E5%BA%93%E8%A7%86%E8%A7%92%E4%B8%8E%E4%BD%8E%E5%BB%B6%E8%BF%9F%E7%B3%BB%E7%BB%9F%E4%B8%AD%E7%9A%84%E7%8E%B0%E5%AE%9E%E5%B7%A5%E7%A8%8B%E8%80%83%E9%87%8F/index.md)
- [1.3.1.5 可运行 C++ 示例：无锁原子累加推进与调度停顿隔离演示](1.3.1.5_%E5%8F%AF%E8%BF%90%E8%A1%8C%20C%2B%2B%20%E7%A4%BA%E4%BE%8B%EF%BC%9A%E6%97%A0%E9%94%81%E5%8E%9F%E5%AD%90%E7%B4%AF%E5%8A%A0%E6%8E%A8%E8%BF%9B%E4%B8%8E%E8%B0%83%E5%BA%A6%E5%81%9C%E9%A1%BF%E9%9A%94%E7%A6%BB%E6%BC%94%E7%A4%BA/index.md)

## 导航

← 上一节：[1.2 并发拓扑与生产者消费者模型  concurrency topologies](../../1.2_并发拓扑与生产者消费者模型_concurrency_topologies/index.md)
↑ 返回上级：[1.3 Lock-Free、Wait-Free 与进度保证  progress guarantees](../index.md)
下一节：[1.3.2 Obstruction-Free：无障碍  obstruction free](../1.3.2_Obstruction-Free：无障碍_obstruction_free/index.md) →
