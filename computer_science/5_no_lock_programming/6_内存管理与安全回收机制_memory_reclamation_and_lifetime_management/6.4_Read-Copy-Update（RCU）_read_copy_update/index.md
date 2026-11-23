# 6.4 Read-Copy-Update（RCU）  read copy update

理解读侧极低开销的更新与回收机制，以及它与普通 C++ 原子操作的关系。

## 本节目录

- [6.4.1 RCU 的设计思想  rcu design principles](6.4.1_RCU%20的设计思想_rcu_design_principles/index.md)
- [6.4.2 RCU Read-Side 与 Update-Side  rcu read side and update side](6.4.2_RCU%20Read-Side%20与%20Update-Side_rcu_read_side_and_update_side/index.md)
- [6.4.3 Grace Period 与 Quiescent State  grace period and quiescent state](6.4.3_Grace%20Period%20与%20Quiescent%20State_grace_period_and_quiescent_state/index.md)
- [6.4.4 RCU 与 C++ 内存模型  rcu and cpp memory model](6.4.4_RCU%20与%20C++%20内存模型_rcu_and_cpp_memory_model/index.md)
- [6.4.5 RCU、EBR 与 Hazard Pointers 比较  rcu ebr hazard pointer comparison](6.4.5_RCU、EBR%20与%20Hazard%20Pointers%20比较_rcu_ebr_hazard_pointer_comparison/index.md)
- [6.4.6 RCU 的适用领域与工程限制  rcu use cases and limits](6.4.6_RCU%20的适用领域与工程限制_rcu_use_cases_and_limits/index.md)

---

## 导航

← 上一节：[6.3 Epoch-Based Reclamation 与 QSBR  epoch based reclamation](../6.3_Epoch-Based%20Reclamation%20与%20QSBR_epoch_based_reclamation/index.md)
↑ 返回上级：[6 内存管理与安全回收机制  memory reclamation and lifetime management](../index.md)
下一节：[6.5 其他内存回收技术  other reclamation techniques](../6.5_其他内存回收技术_other_reclamation_techniques/index.md) →
