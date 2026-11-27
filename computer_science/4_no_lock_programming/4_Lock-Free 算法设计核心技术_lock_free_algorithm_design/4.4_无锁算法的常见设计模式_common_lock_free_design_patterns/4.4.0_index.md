# 4.4 无锁算法的常见设计模式  common lock free design patterns

**介绍**: 归纳可复用的并发算法结构。

## 目录

- [4.4.1 不可变数据与 Copy-On-Write  immutable data and copy on write](4.4.1_%E4%B8%8D%E5%8F%AF%E5%8F%98%E6%95%B0%E6%8D%AE%E4%B8%8E%20Copy-On-Write_immutable_data_and_copy_on_write/index.md)
- [4.4.2 发布后不再修改  publish then immutability](4.4.2_发布后不再修改_publish_then_immutability/index.md)
- [4.4.3 分段与分片状态  sharding and partitioned state](4.4.3_分段与分片状态_sharding_and_partitioned_state/index.md)
- [4.4.4 双缓冲与多版本数据  double buffering and multi version data](4.4.4_双缓冲与多版本数据_double_buffering_and_multi_version_data/index.md)
- [4.4.5 帮助完成机制 Help-Other  help other mechanism](4.4.5_%E5%B8%AE%E5%8A%A9%E5%AE%8C%E6%88%90%E6%9C%BA%E5%88%B6%20Help-Other_help_other_mechanism/index.md)

## 导航

← 上一节：[4.3 ABA 问题与解决方案  aba problem](../4.3_ABA%20%E9%97%AE%E9%A2%98%E4%B8%8E%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88_aba_problem/index.md)
↑ 返回上级：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../index.md)
下一节：[5 经典无锁数据结构与并发拓扑实现  lock free data structures and topologies](../../5_经典无锁数据结构与并发拓扑实现_lock_free_data_structures_and_topologies/index.md) →
