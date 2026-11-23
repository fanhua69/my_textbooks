# 6.3 6.3_Epoch-Based Reclamation 与 QSBR_epoch_based_reclamation

掌握基于 epoch 或静止状态判断旧节点是否可回收的机制。

## 本节目录

- [6.3.1 6.3.1_Epoch-Based Reclamation 基本原理_ebr_basics](6.3.1_Epoch-Based Reclamation 基本原理_ebr_basics/index.md)
- [6.3.2 6.3.2_进入与退出临界区_enter_exit_critical_section](6.3.2_进入与退出临界区_enter_exit_critical_section/index.md)
- [6.3.3 6.3.3_Epoch 推进与安全回收条件_epoch_advancement_and_reclamation](6.3.3_Epoch 推进与安全回收条件_epoch_advancement_and_reclamation/index.md)
- [6.3.4 6.3.4_Quiescent State-Based Reclamation_qsbr](6.3.4_Quiescent State-Based Reclamation_qsbr/index.md)
- [6.3.5 6.3.5_EBR 的线程停顿问题_ebr_stalled_thread_problem](6.3.5_EBR 的线程停顿问题_ebr_stalled_thread_problem/index.md)
- [6.3.6 6.3.6_EBR 的性能与适用场景_ebr_performance_and_use_cases](6.3.6_EBR 的性能与适用场景_ebr_performance_and_use_cases/index.md)

---

## 导航

← 上一节：[6.2 6.2_Hazard Pointers_hazard_pointers](../6.2_Hazard Pointers_hazard_pointers/index.md)
↑ 返回上级：[6 6_内存管理与安全回收机制_memory_reclamation_and_lifetime_management](../index.md)
下一节：[6.4 6.4_Read-Copy-Update（RCU）_read_copy_update](../6.4_Read-Copy-Update（RCU）_read_copy_update/index.md) →
