# 7.1.1 哈希表设计

低延迟场景下哈希表需兼顾平均与最坏性能。

## 本节目录

- [7.1.1.1 开放寻址与探测策略](07.01.1.1_开放寻址与探测策略_OpenAddressingProbing/index.md)
- [7.1.1.2 Swiss Table 与 SIMD 探测](07.01.1.2_Swiss_Table_与_SIMD_探测_SwissTableSIMD/index.md)
- [7.1.1.3 哈希函数选择](07.01.1.3_哈希函数选择_HashFunctionChoice/index.md)
- [7.1.1.4 预分配与无扩容设计](07.01.1.4_预分配与无扩容设计_PreSizedTables/index.md)

---

## 导航

← 上一节：[6 并发编程与无锁技术](../../../06_并发编程与无锁技术_ConcurrencyAndLockFree/index.md)
↑ 返回上级：[7.1 缓存友好的查找结构](../index.md)
下一节：[7.1.2 树与有序结构](../07.01.2_树与有序结构_TreesAndOrderedStructures/index.md) →
