# 1.1.5 锁竞争、上下文切换与优先级反转  lock contention context switch and priority inversion

**介绍**: 分析锁竞争、调度、内核介入、优先级反转及尾延迟。

---

## 小节索引

- [1.1.5.1 锁竞争的成因、微观开销与吞吐退化](./1.1.5.1_锁竞争的成因、微观开销与吞吐退化/index.md)
- [1.1.5.2 上下文切换：用户态、内核态与硬件代价](./1.1.5.2_上下文切换：用户态、内核态与硬件代价/index.md)
- [1.1.5.3 优先级反转：成因、危害与缓解机制](./1.1.5.3_优先级反转：成因、危害与缓解机制/index.md)
- [1.1.5.4 诊断指标与工程观测思路](./1.1.5.4_诊断指标与工程观测思路/index.md)
- [1.1.5.5 可运行 C++ 示例：锁争用与上下文切换对比演示](./1.1.5.5_可运行%20C++%20示例：锁争用与上下文切换对比演示/index.md)

## 导航

← 上一节：[1.1.4 条件变量、信号量与屏障  condition variable semaphore and barrier](../1.1.4_条件变量、信号量与屏障_condition_variable_semaphore_and_barrier/index.md)
↑ 返回上级：[1.1 并发基础与同步原语  concurrency fundamentals](../index.md)
下一节：[1.2 并发拓扑与生产者消费者模型  concurrency topologies](../../1.2_并发拓扑与生产者消费者模型_concurrency_topologies/index.md) →
