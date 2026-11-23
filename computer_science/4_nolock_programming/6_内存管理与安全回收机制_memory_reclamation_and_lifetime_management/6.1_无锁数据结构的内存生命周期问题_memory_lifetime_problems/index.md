# 6.1 6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems

理解并发读取、删除、释放和地址复用之间的冲突。

## 本节目录

- [6.1.1 6.1.1_悬空指针与 Use-After-Free_dangling_pointer_and_uaf](6.1.1_悬空指针与 Use-After-Free_dangling_pointer_and_uaf/index.md)
- [6.1.2 6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation](6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation/index.md)
- [6.1.3 6.1.3_为什么不能直接 delete 节点_why_direct_delete_is_unsafe](6.1.3_为什么不能直接 delete 节点_why_direct_delete_is_unsafe/index.md)
- [6.1.4 6.1.4_内存回收与 ABA 的关系_reclamation_and_aba](6.1.4_内存回收与 ABA 的关系_reclamation_and_aba/index.md)
- [6.1.5 6.1.5_节点生命周期与所有权协议_node_lifetime_and_ownership_protocol](6.1.5_节点生命周期与所有权协议_node_lifetime_and_ownership_protocol/index.md)

---

## 导航

← 上一节：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../../5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies/index.md)
↑ 返回上级：[6 6_内存管理与安全回收机制_memory_reclamation_and_lifetime_management](../index.md)
下一节：[6.2 6.2_Hazard Pointers_hazard_pointers](../6.2_Hazard Pointers_hazard_pointers/index.md) →
