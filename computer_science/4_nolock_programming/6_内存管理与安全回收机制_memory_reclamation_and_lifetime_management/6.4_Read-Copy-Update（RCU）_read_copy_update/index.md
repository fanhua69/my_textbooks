# 6.4 6.4_Read-Copy-Update（RCU）_read_copy_update

理解读侧极低开销的更新与回收机制，以及它与普通 C++ 原子操作的关系。

## 本节目录

- [6.4.1 6.4.1_RCU 的设计思想_rcu_design_principles](6.4.1_RCU 的设计思想_rcu_design_principles/index.md)
- [6.4.2 6.4.2_RCU Read-Side 与 Update-Side_rcu_read_side_and_update_side](6.4.2_RCU Read-Side 与 Update-Side_rcu_read_side_and_update_side/index.md)
- [6.4.3 6.4.3_Grace Period 与 Quiescent State_grace_period_and_quiescent_state](6.4.3_Grace Period 与 Quiescent State_grace_period_and_quiescent_state/index.md)
- [6.4.4 6.4.4_RCU 与 C++ 内存模型_rcu_and_cpp_memory_model](6.4.4_RCU 与 C++ 内存模型_rcu_and_cpp_memory_model/index.md)
- [6.4.5 6.4.5_RCU、EBR 与 Hazard Pointers 比较_rcu_ebr_hazard_pointer_comparison](6.4.5_RCU、EBR 与 Hazard Pointers 比较_rcu_ebr_hazard_pointer_comparison/index.md)
- [6.4.6 6.4.6_RCU 的适用领域与工程限制_rcu_use_cases_and_limits](6.4.6_RCU 的适用领域与工程限制_rcu_use_cases_and_limits/index.md)

---

## 导航

← 上一节：[6.3 6.3_Epoch-Based Reclamation 与 QSBR_epoch_based_reclamation](../6.3_Epoch-Based Reclamation 与 QSBR_epoch_based_reclamation/index.md)
↑ 返回上级：[6 6_内存管理与安全回收机制_memory_reclamation_and_lifetime_management](../index.md)
下一节：[6.5 6.5_其他内存回收技术_other_reclamation_techniques](../6.5_其他内存回收技术_other_reclamation_techniques/index.md) →
