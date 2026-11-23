# 6.1.1 6.1.1_悬空指针与 Use-After-Free_dangling_pointer_and_uaf

分析线程仍持有节点指针而另一个线程已释放对象的危险。

---

## 导航

← 上一节：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../../../5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies/index.md)
↑ 返回上级：[6.1 6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems](../index.md)
下一节：[6.1.2 6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation](../6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation/index.md) →
