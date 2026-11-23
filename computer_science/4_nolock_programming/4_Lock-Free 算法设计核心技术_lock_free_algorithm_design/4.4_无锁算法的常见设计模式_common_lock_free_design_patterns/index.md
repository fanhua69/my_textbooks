# 4.4 4.4_无锁算法的常见设计模式_common_lock_free_design_patterns

归纳可复用的并发算法结构。

## 本节目录

- [4.4.1 4.4.1_不可变数据与 Copy-On-Write_immutable_data_and_copy_on_write](4.4.1_不可变数据与 Copy-On-Write_immutable_data_and_copy_on_write/index.md)
- [4.4.2 4.4.2_发布后不再修改_publish_then_immutability](4.4.2_发布后不再修改_publish_then_immutability/index.md)
- [4.4.3 4.4.3_分段与分片状态_sharding_and_partitioned_state](4.4.3_分段与分片状态_sharding_and_partitioned_state/index.md)
- [4.4.4 4.4.4_双缓冲与多版本数据_double_buffering_and_multi_version_data](4.4.4_双缓冲与多版本数据_double_buffering_and_multi_version_data/index.md)
- [4.4.5 4.4.5_帮助完成机制 Help-Other_help_other_mechanism](4.4.5_帮助完成机制 Help-Other_help_other_mechanism/index.md)

---

## 导航

← 上一节：[4.3 4.3_ABA 问题与解决方案_aba_problem](../4.3_ABA 问题与解决方案_aba_problem/index.md)
↑ 返回上级：[4 4_Lock-Free 算法设计核心技术_lock_free_algorithm_design](../index.md)
下一节：[5 5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies](../../5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies/index.md) →
