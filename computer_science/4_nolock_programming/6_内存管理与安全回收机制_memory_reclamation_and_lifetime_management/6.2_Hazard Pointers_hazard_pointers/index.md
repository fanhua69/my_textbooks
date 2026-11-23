# 6.2 6.2_Hazard Pointers_hazard_pointers

掌握通过线程声明正在访问的节点，阻止其他线程过早回收的机制。

## 本节目录

- [6.2.1 6.2.1_Hazard Pointer 基本思想_hazard_pointer_basics](6.2.1_Hazard Pointer 基本思想_hazard_pointer_basics/index.md)
- [6.2.2 6.2.2_发布 Hazard Pointer 的正确顺序_hazard_pointer_publication_order](6.2.2_发布 Hazard Pointer 的正确顺序_hazard_pointer_publication_order/index.md)
- [6.2.3 6.2.3_扫描 Hazard Records 与延迟释放_scan_hazard_records](6.2.3_扫描 Hazard Records 与延迟释放_scan_hazard_records/index.md)
- [6.2.4 6.2.4_Hazard Pointer Stack 实现_hazard_pointer_stack](6.2.4_Hazard Pointer Stack 实现_hazard_pointer_stack/index.md)
- [6.2.5 6.2.5_Hazard Pointer Queue 实现_hazard_pointer_queue](6.2.5_Hazard Pointer Queue 实现_hazard_pointer_queue/index.md)
- [6.2.6 6.2.6_Hazard Pointer 的性能与局限_hazard_pointer_costs_and_limits](6.2.6_Hazard Pointer 的性能与局限_hazard_pointer_costs_and_limits/index.md)

---

## 导航

← 上一节：[6.1 6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems](../6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems/index.md)
↑ 返回上级：[6 6_内存管理与安全回收机制_memory_reclamation_and_lifetime_management](../index.md)
下一节：[6.3 6.3_Epoch-Based Reclamation 与 QSBR_epoch_based_reclamation](../6.3_Epoch-Based Reclamation 与 QSBR_epoch_based_reclamation/index.md) →
