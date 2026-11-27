# 6.1 无锁数据结构的内存生命周期问题  memory lifetime problems

**介绍**: 理解并发读取、删除、释放和地址复用之间的冲突。

## 目录

- [6.1.1 悬空指针与 Use-After-Free  dangling pointer and uaf](6.1.1_%E6%82%AC%E7%A9%BA%E6%8C%87%E9%92%88%E4%B8%8E%20Use-After-Free_dangling_pointer_and_uaf/index.md)
- [6.1.2 逻辑删除与物理回收  logical deletion and physical reclamation](6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation/index.md)
- [6.1.3 为什么不能直接 delete 节点  why direct delete is unsafe](6.1.3_%E4%B8%BA%E4%BB%80%E4%B9%88%E4%B8%8D%E8%83%BD%E7%9B%B4%E6%8E%A5%20delete%20%E8%8A%82%E7%82%B9_why_direct_delete_is_unsafe/index.md)
- [6.1.4 内存回收与 ABA 的关系  reclamation and aba](6.1.4_%E5%86%85%E5%AD%98%E5%9B%9E%E6%94%B6%E4%B8%8E%20ABA%20%E7%9A%84%E5%85%B3%E7%B3%BB_reclamation_and_aba/index.md)
- [6.1.5 节点生命周期与所有权协议  node lifetime and ownership protocol](6.1.5_节点生命周期与所有权协议_node_lifetime_and_ownership_protocol/index.md)

## 导航

← 上一节：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../../5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies/index.md)
↑ 返回上级：[6 内存管理与安全回收机制  memory reclamation and lifetime management](../index.md)
下一节：[6.2 Hazard Pointers  hazard pointers](../6.2_Hazard%20Pointers_hazard_pointers/index.md) →
