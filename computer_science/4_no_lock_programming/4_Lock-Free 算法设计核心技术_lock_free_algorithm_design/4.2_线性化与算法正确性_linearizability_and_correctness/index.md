# 4.2 线性化与算法正确性  linearizability and correctness

用形式化并发语义描述操作是否正确。

## 本节目录

- [4.2.1 Linearizability：线性化  linearizability](4.2.1_Linearizability：线性化_linearizability/index.md)
- [4.2.2 Linearization Point：线性化点  linearization point](4.2.2_Linearization%20Point：线性化点_linearization_point/index.md)
- [4.2.3 Sequential Consistency 与 Linearizability 的区别  sequential consistency vs linearizability](4.2.3_Sequential%20Consistency%20与%20Linearizability%20的区别_sequential_consistency_vs_linearizability/index.md)
- [4.2.4 Safety 与 Liveness  safety and liveness](4.2.4_Safety%20与%20Liveness_safety_and_liveness/index.md)
- [4.2.5 不变量与状态转换证明  invariants and state transition proofs](4.2.5_不变量与状态转换证明_invariants_and_state_transition_proofs/index.md)
- [4.2.6 并发历史与操作重排验证  concurrent histories](4.2.6_并发历史与操作重排验证_concurrent_histories/index.md)

---

## 导航

← 上一节：[4.1 CAS 循环与状态更新  cas loops and state updates](../4.1_CAS%20循环与状态更新_cas_loops_and_state_updates/index.md)
↑ 返回上级：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../index.md)
下一节：[4.3 ABA 问题与解决方案  aba problem](../4.3_ABA%20问题与解决方案_aba_problem/index.md) →
