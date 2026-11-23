# 4.3 ABA 问题与解决方案  aba problem

深入理解 CAS 只比较位模式所造成的状态误判及其缓解方案。

## 本节目录

- [4.3.1 ABA 问题的产生过程  aba problem walkthrough](4.3.1_ABA%20问题的产生过程_aba_problem_walkthrough/index.md)
- [4.3.2 指针复用与内存释放导致的 ABA  pointer reuse and reclamation](4.3.2_指针复用与内存释放导致的%20ABA_pointer_reuse_and_reclamation/index.md)
- [4.3.3 Tagged Pointer 与版本计数  tagged pointer and version counter](4.3.3_Tagged%20Pointer%20与版本计数_tagged_pointer_and_version_counter/index.md)
- [4.3.4 Double-Width CAS  double width cas](4.3.4_Double-Width%20CAS_double_width_cas/index.md)
- [4.3.5 ABA 的其他处理策略  other aba mitigation](4.3.5_ABA%20的其他处理策略_other_aba_mitigation/index.md)

---

## 导航

← 上一节：[4.2 线性化与算法正确性  linearizability and correctness](../4.2_线性化与算法正确性_linearizability_and_correctness/index.md)
↑ 返回上级：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../index.md)
下一节：[4.4 无锁算法的常见设计模式  common lock free design patterns](../4.4_无锁算法的常见设计模式_common_lock_free_design_patterns/index.md) →
