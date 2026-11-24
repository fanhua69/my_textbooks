# 6.1.3 为什么不能直接 delete 节点  why direct delete is unsafe

**介绍**: 用线程交错案例展示直接释放造成的崩溃和未定义行为。

---

## 导航

← 上一节：[6.1.2 逻辑删除与物理回收  logical deletion and physical reclamation](../6.1.2_逻辑删除与物理回收_logical_deletion_and_physical_reclamation/index.md)
↑ 返回上级：[6.1 无锁数据结构的内存生命周期问题  memory lifetime problems](../index.md)
下一节：[6.1.4 内存回收与 ABA 的关系  reclamation and aba](../6.1.4_%E5%86%85%E5%AD%98%E5%9B%9E%E6%94%B6%E4%B8%8E%20ABA%20%E7%9A%84%E5%85%B3%E7%B3%BB_reclamation_and_aba/index.md) →
