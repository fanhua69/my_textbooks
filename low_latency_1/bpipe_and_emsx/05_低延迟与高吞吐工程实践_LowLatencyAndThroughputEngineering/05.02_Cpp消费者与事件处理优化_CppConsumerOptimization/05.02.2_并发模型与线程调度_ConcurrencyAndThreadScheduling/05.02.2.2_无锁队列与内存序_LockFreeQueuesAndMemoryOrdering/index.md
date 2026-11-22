# 5.2.2.2 无锁队列与内存序

使用 acquire/release 等内存序实现生产者消费者队列，并分析伪共享、ABA 和进度保证。

---

## 导航

← 上一节：[5.2.2.1 事件循环与线程分区](../05.02.2.1_事件循环与线程分区_EventLoopAndThreadPartitioning/index.md)
↑ 返回上级：[5.2.2 并发模型与线程调度](../index.md)
下一节：[5.2.2.3 CPU 亲和性与 NUMA](../05.02.2.3_CPU亲和性与NUMA_CPUAffinityAndNUMA/index.md) →
