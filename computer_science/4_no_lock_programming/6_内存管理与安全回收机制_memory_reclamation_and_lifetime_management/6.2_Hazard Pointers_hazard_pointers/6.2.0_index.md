# 6.2 Hazard Pointers  hazard pointers

**介绍**: 掌握通过线程声明正在访问的节点，阻止其他线程过早回收的机制。

## 目录

- [6.2.1 Hazard Pointer 基本思想  hazard pointer basics](6.2.1_Hazard%20Pointer%20%E5%9F%BA%E6%9C%AC%E6%80%9D%E6%83%B3_hazard_pointer_basics/index.md)
- [6.2.2 发布 Hazard Pointer 的正确顺序  hazard pointer publication order](6.2.2_%E5%8F%91%E5%B8%83%20Hazard%20Pointer%20%E7%9A%84%E6%AD%A3%E7%A1%AE%E9%A1%BA%E5%BA%8F_hazard_pointer_publication_order/index.md)
- [6.2.3 扫描 Hazard Records 与延迟释放  scan hazard records](6.2.3_%E6%89%AB%E6%8F%8F%20Hazard%20Records%20%E4%B8%8E%E5%BB%B6%E8%BF%9F%E9%87%8A%E6%94%BE_scan_hazard_records/index.md)
- [6.2.4 Hazard Pointer Stack 实现  hazard pointer stack](6.2.4_Hazard%20Pointer%20Stack%20%E5%AE%9E%E7%8E%B0_hazard_pointer_stack/index.md)
- [6.2.5 Hazard Pointer Queue 实现  hazard pointer queue](6.2.5_Hazard%20Pointer%20Queue%20%E5%AE%9E%E7%8E%B0_hazard_pointer_queue/index.md)
- [6.2.6 Hazard Pointer 的性能与局限  hazard pointer costs and limits](6.2.6_Hazard%20Pointer%20%E7%9A%84%E6%80%A7%E8%83%BD%E4%B8%8E%E5%B1%80%E9%99%90_hazard_pointer_costs_and_limits/index.md)

## 导航

← 上一节：[6.1 无锁数据结构的内存生命周期问题  memory lifetime problems](../6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems/index.md)
↑ 返回上级：[6 内存管理与安全回收机制  memory reclamation and lifetime management](../index.md)
下一节：[6.3 Epoch-Based Reclamation 与 QSBR  epoch based reclamation](../6.3_Epoch-Based%20Reclamation%20%E4%B8%8E%20QSBR_epoch_based_reclamation/index.md) →
