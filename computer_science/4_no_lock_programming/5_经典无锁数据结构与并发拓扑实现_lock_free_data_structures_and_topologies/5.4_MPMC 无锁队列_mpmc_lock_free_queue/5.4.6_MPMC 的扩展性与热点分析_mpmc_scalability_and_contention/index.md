# 5.4.6 MPMC 的扩展性与热点分析  mpmc scalability and contention

**介绍**: 分析 CAS 重试、缓存行争用、NUMA 和线程数扩展。

---

## 导航

← 上一节：[5.4.5 MPMC 的线性化点与正确性  mpmc linearization and correctness](../5.4.5_MPMC%20%E7%9A%84%E7%BA%BF%E6%80%A7%E5%8C%96%E7%82%B9%E4%B8%8E%E6%AD%A3%E7%A1%AE%E6%80%A7_mpmc_linearization_and_correctness/index.md)
↑ 返回上级：[5.4 MPMC 无锁队列  mpmc lock free queue](../index.md)
下一节：[5.5 SPMC 与广播/扇出结构  spmc and broadcast queues](../../5.5_SPMC%20%E4%B8%8E%E5%B9%BF%E6%92%AD_%E6%89%87%E5%87%BA%E7%BB%93%E6%9E%84_spmc_and_broadcast_queues/index.md) →
