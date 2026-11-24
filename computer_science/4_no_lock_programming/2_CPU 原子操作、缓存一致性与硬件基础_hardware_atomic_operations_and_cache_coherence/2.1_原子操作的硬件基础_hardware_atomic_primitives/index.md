# 2.1 原子操作的硬件基础  hardware atomic primitives

**介绍**: 理解处理器提供的原子指令及其约束。

## 目录

- [2.1.1 原子性、可见性与有序性  atomicity visibility and ordering](2.1.1_原子性、可见性与有序性_atomicity_visibility_and_ordering/index.md)
- [2.1.2 Read-Modify-Write 操作  read modify write](2.1.2_Read-Modify-Write%20%E6%93%8D%E4%BD%9C_read_modify_write/index.md)
- [2.1.3 Compare-And-Swap 与 Compare-And-Exchange  cas and compare exchange](2.1.3_Compare-And-Swap%20%E4%B8%8E%20Compare-And-Exchange_cas_and_compare_exchange/index.md)
- [2.1.4 Test-And-Set、Fetch-And-Add 与交换指令  test and set fetch add and exchange](2.1.4_Test-And-Set%E3%80%81Fetch-And-Add%20%E4%B8%8E%E4%BA%A4%E6%8D%A2%E6%8C%87%E4%BB%A4_test_and_set_fetch_add_and_exchange/index.md)
- [2.1.5 x86-64 与 ARM64 原子指令概览  x86 64 and arm64 atomic instructions](2.1.5_x86-64%20%E4%B8%8E%20ARM64%20%E5%8E%9F%E5%AD%90%E6%8C%87%E4%BB%A4%E6%A6%82%E8%A7%88_x86_64_and_arm64_atomic_instructions/index.md)
- [2.1.6 原子操作是否真的 Lock-Free  hardware lock free support](2.1.6_%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C%E6%98%AF%E5%90%A6%E7%9C%9F%E7%9A%84%20Lock-Free_hardware_lock_free_support/index.md)

## 导航

← 上一节：[1 无锁编程基础与并发模型  lock free fundamentals and concurrency models](../../1_无锁编程基础与并发模型_lock_free_fundamentals_and_concurrency_models/index.md)
↑ 返回上级：[2 CPU 原子操作、缓存一致性与硬件基础  hardware atomic operations and cache coherence](../index.md)
下一节：[2.2 缓存一致性与多核通信  cache coherence and intercore communication](../2.2_缓存一致性与多核通信_cache_coherence_and_intercore_communication/index.md) →
