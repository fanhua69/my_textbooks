# 4.3 4.3_ABA 问题与解决方案_aba_problem

深入理解 CAS 只比较位模式所造成的状态误判及其缓解方案。

## 本节目录

- [4.3.1 4.3.1_ABA 问题的产生过程_aba_problem_walkthrough](4.3.1_ABA 问题的产生过程_aba_problem_walkthrough/index.md)
- [4.3.2 4.3.2_指针复用与内存释放导致的 ABA_pointer_reuse_and_reclamation](4.3.2_指针复用与内存释放导致的 ABA_pointer_reuse_and_reclamation/index.md)
- [4.3.3 4.3.3_Tagged Pointer 与版本计数_tagged_pointer_and_version_counter](4.3.3_Tagged Pointer 与版本计数_tagged_pointer_and_version_counter/index.md)
- [4.3.4 4.3.4_Double-Width CAS_double_width_cas](4.3.4_Double-Width CAS_double_width_cas/index.md)
- [4.3.5 4.3.5_ABA 的其他处理策略_other_aba_mitigation](4.3.5_ABA 的其他处理策略_other_aba_mitigation/index.md)

---

## 导航

← 上一节：[4.2 4.2_线性化与算法正确性_linearizability_and_correctness](../4.2_线性化与算法正确性_linearizability_and_correctness/index.md)
↑ 返回上级：[4 4_Lock-Free 算法设计核心技术_lock_free_algorithm_design](../index.md)
下一节：[4.4 4.4_无锁算法的常见设计模式_common_lock_free_design_patterns](../4.4_无锁算法的常见设计模式_common_lock_free_design_patterns/index.md) →
