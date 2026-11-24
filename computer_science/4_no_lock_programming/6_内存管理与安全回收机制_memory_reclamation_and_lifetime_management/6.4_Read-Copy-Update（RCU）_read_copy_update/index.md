# 6.4 Read-Copy-Update（RCU）  read copy update

**介绍**: 理解读侧极低开销的更新与回收机制，以及它与普通 C++ 原子操作的关系。

## 目录

- [6.4.1 RCU 的设计思想  rcu design principles](6.4.1_RCU%20%E7%9A%84%E8%AE%BE%E8%AE%A1%E6%80%9D%E6%83%B3_rcu_design_principles/index.md)
- [6.4.2 RCU Read-Side 与 Update-Side  rcu read side and update side](6.4.2_RCU%20Read-Side%20%E4%B8%8E%20Update-Side_rcu_read_side_and_update_side/index.md)
- [6.4.3 Grace Period 与 Quiescent State  grace period and quiescent state](6.4.3_Grace%20Period%20%E4%B8%8E%20Quiescent%20State_grace_period_and_quiescent_state/index.md)
- [6.4.4 RCU 与 C++ 内存模型  rcu and cpp memory model](6.4.4_RCU%20%E4%B8%8E%20C%2B%2B%20%E5%86%85%E5%AD%98%E6%A8%A1%E5%9E%8B_rcu_and_cpp_memory_model/index.md)
- [6.4.5 RCU、EBR 与 Hazard Pointers 比较  rcu ebr hazard pointer comparison](6.4.5_RCU%E3%80%81EBR%20%E4%B8%8E%20Hazard%20Pointers%20%E6%AF%94%E8%BE%83_rcu_ebr_hazard_pointer_comparison/index.md)
- [6.4.6 RCU 的适用领域与工程限制  rcu use cases and limits](6.4.6_RCU%20%E7%9A%84%E9%80%82%E7%94%A8%E9%A2%86%E5%9F%9F%E4%B8%8E%E5%B7%A5%E7%A8%8B%E9%99%90%E5%88%B6_rcu_use_cases_and_limits/index.md)

## 导航

← 上一节：[6.3 Epoch-Based Reclamation 与 QSBR  epoch based reclamation](../6.3_Epoch-Based%20Reclamation%20与%20QSBR_epoch_based_reclamation/index.md)
↑ 返回上级：[6 内存管理与安全回收机制  memory reclamation and lifetime management](../index.md)
下一节：[6.5 其他内存回收技术  other reclamation techniques](../6.5_其他内存回收技术_other_reclamation_techniques/index.md) →
