# 6.3 Epoch-Based Reclamation 与 QSBR  epoch based reclamation

**介绍**: 掌握基于 epoch 或静止状态判断旧节点是否可回收的机制。

## 目录

- [6.3.1 Epoch-Based Reclamation 基本原理  ebr basics](6.3.1_Epoch-Based%20Reclamation%20%E5%9F%BA%E6%9C%AC%E5%8E%9F%E7%90%86_ebr_basics/index.md)
- [6.3.2 进入与退出临界区  enter exit critical section](6.3.2_进入与退出临界区_enter_exit_critical_section/index.md)
- [6.3.3 Epoch 推进与安全回收条件  epoch advancement and reclamation](6.3.3_Epoch%20%E6%8E%A8%E8%BF%9B%E4%B8%8E%E5%AE%89%E5%85%A8%E5%9B%9E%E6%94%B6%E6%9D%A1%E4%BB%B6_epoch_advancement_and_reclamation/index.md)
- [6.3.4 Quiescent State-Based Reclamation  qsbr](6.3.4_Quiescent%20State-Based%20Reclamation_qsbr/index.md)
- [6.3.5 EBR 的线程停顿问题  ebr stalled thread problem](6.3.5_EBR%20%E7%9A%84%E7%BA%BF%E7%A8%8B%E5%81%9C%E9%A1%BF%E9%97%AE%E9%A2%98_ebr_stalled_thread_problem/index.md)
- [6.3.6 EBR 的性能与适用场景  ebr performance and use cases](6.3.6_EBR%20%E7%9A%84%E6%80%A7%E8%83%BD%E4%B8%8E%E9%80%82%E7%94%A8%E5%9C%BA%E6%99%AF_ebr_performance_and_use_cases/index.md)

## 导航

← 上一节：[6.2 Hazard Pointers  hazard pointers](../6.2_Hazard%20Pointers_hazard_pointers/index.md)
↑ 返回上级：[6 内存管理与安全回收机制  memory reclamation and lifetime management](../index.md)
下一节：[6.4 Read-Copy-Update（RCU）  read copy update](../6.4_Read-Copy-Update（RCU）_read_copy_update/index.md) →
