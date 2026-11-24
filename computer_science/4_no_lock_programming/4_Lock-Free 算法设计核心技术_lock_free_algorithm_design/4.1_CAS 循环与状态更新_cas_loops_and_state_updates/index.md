# 4.1 CAS 循环与状态更新  cas loops and state updates

**介绍**: 掌握以 compare-exchange 构建并发状态转换的基本方法。

## 目录

- [4.1.1 CAS Retry Loop 基本模式  cas retry loop](4.1.1_CAS%20Retry%20Loop%20%E5%9F%BA%E6%9C%AC%E6%A8%A1%E5%BC%8F_cas_retry_loop/index.md)
- [4.1.2 Weak CAS 与 Strong CAS 的选择  weak vs strong cas](4.1.2_Weak%20CAS%20%E4%B8%8E%20Strong%20CAS%20%E7%9A%84%E9%80%89%E6%8B%A9_weak_vs_strong_cas/index.md)
- [4.1.3 竞争失败与 Backoff 策略  contention and backoff](4.1.3_%E7%AB%9E%E4%BA%89%E5%A4%B1%E8%B4%A5%E4%B8%8E%20Backoff%20%E7%AD%96%E7%95%A5_contention_and_backoff/index.md)
- [4.1.4 状态机与原子状态转换  atomic state machine](4.1.4_状态机与原子状态转换_atomic_state_machine/index.md)
- [4.1.5 多字段状态与打包原子状态  packed atomic state](4.1.5_多字段状态与打包原子状态_packed_atomic_state/index.md)

## 导航

← 上一节：[3 C++ 原子库与内存模型  cpp atomics and memory model](../../3_C++%20原子库与内存模型_cpp_atomics_and_memory_model/index.md)
↑ 返回上级：[4 Lock-Free 算法设计核心技术  lock free algorithm design](../index.md)
下一节：[4.2 线性化与算法正确性  linearizability and correctness](../4.2_线性化与算法正确性_linearizability_and_correctness/index.md) →
