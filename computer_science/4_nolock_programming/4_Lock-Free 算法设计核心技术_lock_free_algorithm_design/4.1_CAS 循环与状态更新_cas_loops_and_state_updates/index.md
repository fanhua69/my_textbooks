# 4.1 4.1_CAS 循环与状态更新_cas_loops_and_state_updates

掌握以 compare-exchange 构建并发状态转换的基本方法。

## 本节目录

- [4.1.1 4.1.1_CAS Retry Loop 基本模式_cas_retry_loop](4.1.1_CAS Retry Loop 基本模式_cas_retry_loop/index.md)
- [4.1.2 4.1.2_Weak CAS 与 Strong CAS 的选择_weak_vs_strong_cas](4.1.2_Weak CAS 与 Strong CAS 的选择_weak_vs_strong_cas/index.md)
- [4.1.3 4.1.3_竞争失败与 Backoff 策略_contention_and_backoff](4.1.3_竞争失败与 Backoff 策略_contention_and_backoff/index.md)
- [4.1.4 4.1.4_状态机与原子状态转换_atomic_state_machine](4.1.4_状态机与原子状态转换_atomic_state_machine/index.md)
- [4.1.5 4.1.5_多字段状态与打包原子状态_packed_atomic_state](4.1.5_多字段状态与打包原子状态_packed_atomic_state/index.md)

---

## 导航

← 上一节：[3 3_C++ 原子库与内存模型_cpp_atomics_and_memory_model](../../3_C++ 原子库与内存模型_cpp_atomics_and_memory_model/index.md)
↑ 返回上级：[4 4_Lock-Free 算法设计核心技术_lock_free_algorithm_design](../index.md)
下一节：[4.2 4.2_线性化与算法正确性_linearizability_and_correctness](../4.2_线性化与算法正确性_linearizability_and_correctness/index.md) →
