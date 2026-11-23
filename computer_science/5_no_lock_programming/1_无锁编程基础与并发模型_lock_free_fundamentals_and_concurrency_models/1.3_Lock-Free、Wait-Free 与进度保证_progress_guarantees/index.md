# 1.3 Lock-Free、Wait-Free 与进度保证  progress guarantees

严格定义非阻塞算法的进度属性，避免把无锁、无等待和无互斥锁混为一谈。

## 本节目录

- [1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms](1.3.1_Blocking%20与%20Non-blocking%20算法_blocking_and_non_blocking_algorithms/index.md)
- [1.3.2 Obstruction-Free：无障碍  obstruction free](1.3.2_Obstruction-Free：无障碍_obstruction_free/index.md)
- [1.3.3 Lock-Free：无锁  lock free](1.3.3_Lock-Free：无锁_lock_free/index.md)
- [1.3.4 Wait-Free：无等待  wait free](1.3.4_Wait-Free：无等待_wait_free/index.md)
- [1.3.5 公平性、饥饿与活锁  fairness starvation and livelock](1.3.5_公平性、饥饿与活锁_fairness_starvation_and_livelock/index.md)
- [1.3.6 Lock-Free 不等于使用 atomic  lock free is not just atomic](1.3.6_Lock-Free%20不等于使用%20atomic_lock_free_is_not_just_atomic/index.md)

---

## 导航

← 上一节：[1.2 并发拓扑与生产者消费者模型  concurrency topologies](../1.2_并发拓扑与生产者消费者模型_concurrency_topologies/index.md)
↑ 返回上级：[1 无锁编程基础与并发模型  lock free fundamentals and concurrency models](../index.md)
下一节：[1.4 无锁编程的适用边界  when to use lock free](../1.4_无锁编程的适用边界_when_to_use_lock_free/index.md) →
