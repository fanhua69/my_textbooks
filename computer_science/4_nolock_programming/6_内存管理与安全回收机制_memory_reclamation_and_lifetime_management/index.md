# 6 6_内存管理与安全回收机制_memory_reclamation_and_lifetime_management

无锁数据结构最难的部分往往不是 CAS，而是节点何时可以安全释放。本部分系统比较 Hazard Pointers、Epoch-Based Reclamation、RCU 等技术。

## 本节目录

- [6.1 6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems](6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems/index.md)
- [6.2 6.2_Hazard Pointers_hazard_pointers](6.2_Hazard Pointers_hazard_pointers/index.md)
- [6.3 6.3_Epoch-Based Reclamation 与 QSBR_epoch_based_reclamation](6.3_Epoch-Based Reclamation 与 QSBR_epoch_based_reclamation/index.md)
- [6.4 6.4_Read-Copy-Update（RCU）_read_copy_update](6.4_Read-Copy-Update（RCU）_read_copy_update/index.md)
- [6.5 6.5_其他内存回收技术_other_reclamation_techniques](6.5_其他内存回收技术_other_reclamation_techniques/index.md)

---

## 导航

← 上一节：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies/index.md)
↑ 返回上级：[No-Lock Programming：C++ 无锁编程](../index.md)
下一节：[7 7_无锁编程性能工程与系统优化_lock_free_performance_engineering](../7_无锁编程性能工程与系统优化_lock_free_performance_engineering/index.md) →
