# 4.4 无锁算法的常见设计模式  common lock free design patterns

归纳可复用的并发算法结构。

## 本节目录

- [4.4.1 不可变数据与 Copy-On-Write  immutable data and copy on write](4.4.1_不可变数据与%20Copy-On-Write_immutable_data_and_copy_on_write/index.md)
- [4.4.2 发布后不再修改  publish then immutability](4.4.2_发布后不再修改_publish_then_immutability/index.md)
- [4.4.3 分段与分片状态  sharding and partitioned state](4.4.3_分段与分片状态_sharding_and_partitioned_state/index.md)
- [4.4.4 双缓冲与多版本数据  double buffering and multi version data](4.4.4_双缓冲与多版本数据_double_buffering_and_multi_version_data/index.md)
- [4.4.5 帮助完成机制 Help-Other  help other mechanism](4.4.5_帮助完成机制%20Help-Other_help_other_mechanism/index.md)

---

## 导航

← 上一节：[4.3 ABA 问题与解决方案  aba problem](../4.3_ABA%20问题与解决方案_aba_problem/index.md)
↑ 返回上级：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../index.md)
下一节：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../../5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies/index.md) →
