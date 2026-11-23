# 5.3.2 5.3.2_基于 CAS 的 MPSC 入队_mpsc_cas_enqueue

分析多个生产者争夺尾指针、节点链接和发布顺序。

---

## 导航

← 上一节：[5.3.1 5.3.1_MPSC 的并发约束与典型场景_mpsc_constraints_and_use_cases](../5.3.1_MPSC 的并发约束与典型场景_mpsc_constraints_and_use_cases/index.md)
↑ 返回上级：[5.3 5.3_MPSC 无锁队列_mpsc_lock_free_queue](../index.md)
下一节：[5.3.3 5.3.3_单消费者出队路径_mpsc_single_consumer_dequeue](../5.3.3_单消费者出队路径_mpsc_single_consumer_dequeue/index.md) →
