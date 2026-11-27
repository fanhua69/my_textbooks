# 2.3.5 原子操作的硬件代价  cost of atomic operations

**介绍**: 分析原子读、写、RMW、屏障和缓存行迁移的相对成本。

---

## 导航

← 上一节：[2.3.4 x86-TSO 与 ARM 弱内存模型  x86 tso and arm weak memory model](../2.3.4_x86-TSO%20%E4%B8%8E%20ARM%20%E5%BC%B1%E5%86%85%E5%AD%98%E6%A8%A1%E5%9E%8B_x86_tso_and_arm_weak_memory_model/index.md)
↑ 返回上级：[2.3 内存屏障与处理器内存模型  hardware memory ordering](../index.md)
下一节：[3 C++ 原子库与内存模型  cpp atomics and memory model](../../../3_C%2B%2B%20%E5%8E%9F%E5%AD%90%E5%BA%93%E4%B8%8E%E5%86%85%E5%AD%98%E6%A8%A1%E5%9E%8B_cpp_atomics_and_memory_model/index.md) →
