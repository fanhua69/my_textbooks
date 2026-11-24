# 5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies

**介绍**: 围绕常见数据结构和生产者消费者拓扑展开实现与比较。每种结构都分析有界/无界版本、线性化点、内存序、内存回收和性能特征。

## 目录

- [5.1 Ring Buffer 与循环队列  ring buffer and circular queue](5.1_Ring%20Buffer%20%E4%B8%8E%E5%BE%AA%E7%8E%AF%E9%98%9F%E5%88%97_ring_buffer_and_circular_queue/index.md)
- [5.2 SPSC 无锁队列  spsc lock free queue](5.2_SPSC%20%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97_spsc_lock_free_queue/index.md)
- [5.3 MPSC 无锁队列  mpsc lock free queue](5.3_MPSC%20%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97_mpsc_lock_free_queue/index.md)
- [5.4 MPMC 无锁队列  mpmc lock free queue](5.4_MPMC%20%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97_mpmc_lock_free_queue/index.md)
- [5.5 SPMC 与广播/扇出结构  spmc and broadcast queues](5.5_SPMC%20%E4%B8%8E%E5%B9%BF%E6%92%AD_%E6%89%87%E5%87%BA%E7%BB%93%E6%9E%84_spmc_and_broadcast_queues/index.md)
- [5.6 其他常见无锁数据结构  other lock free data structures](5.6_其他常见无锁数据结构_other_lock_free_data_structures/index.md)

## 导航

← 上一节：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../4_Lock-Free%20%E7%AE%97%E6%B3%95%E8%AE%BE%E8%AE%A1%E6%A0%B8%E5%BF%83%E6%8A%80%E6%9C%AF_lock_free_algorithm_design/index.md)
↑ 返回上级：[No-Lock Programming：C++ 无锁编程](../index.md)
下一节：[6 内存管理与安全回收机制  memory reclamation and lifetime management](../6_内存管理与安全回收机制_memory_reclamation_and_lifetime_management/index.md) →
