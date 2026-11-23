# 6.1.3 6.1.3_为什么不能直接 delete 节点_why_direct_delete_is_unsafe

用线程交错案例展示直接释放造成的崩溃和未定义行为。

---

## 导航

← 上一节：[6.1.2 6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation](../6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation/index.md)
↑ 返回上级：[6.1 6.1_无锁数据结构的内存生命周期问题_memory_lifetime_problems](../index.md)
下一节：[6.1.4 6.1.4_内存回收与 ABA 的关系_reclamation_and_aba](../6.1.4_内存回收与 ABA 的关系_reclamation_and_aba/index.md) →
