# 1.3 1.3_Lock-Free、Wait-Free 与进度保证_progress_guarantees

严格定义非阻塞算法的进度属性，避免把无锁、无等待和无互斥锁混为一谈。

## 本节目录

- [1.3.1 1.3.1_Blocking 与 Non-blocking 算法_blocking_and_non_blocking_algorithms](1.3.1_Blocking 与 Non-blocking 算法_blocking_and_non_blocking_algorithms/index.md)
- [1.3.2 1.3.2_Obstruction-Free：无障碍_obstruction_free](1.3.2_Obstruction-Free：无障碍_obstruction_free/index.md)
- [1.3.3 1.3.3_Lock-Free：无锁_lock_free](1.3.3_Lock-Free：无锁_lock_free/index.md)
- [1.3.4 1.3.4_Wait-Free：无等待_wait_free](1.3.4_Wait-Free：无等待_wait_free/index.md)
- [1.3.5 1.3.5_公平性、饥饿与活锁_fairness_starvation_and_livelock](1.3.5_公平性、饥饿与活锁_fairness_starvation_and_livelock/index.md)
- [1.3.6 1.3.6_Lock-Free 不等于使用 atomic_lock_free_is_not_just_atomic](1.3.6_Lock-Free 不等于使用 atomic_lock_free_is_not_just_atomic/index.md)

---

## 导航

← 上一节：[1.2 1.2_并发拓扑与生产者消费者模型_concurrency_topologies](../1.2_并发拓扑与生产者消费者模型_concurrency_topologies/index.md)
↑ 返回上级：[1 1_无锁编程基础与并发模型_lock_free_fundamentals_and_concurrency_models](../index.md)
下一节：[1.4 1.4_无锁编程的适用边界_when_to_use_lock_free](../1.4_无锁编程的适用边界_when_to_use_lock_free/index.md) →
