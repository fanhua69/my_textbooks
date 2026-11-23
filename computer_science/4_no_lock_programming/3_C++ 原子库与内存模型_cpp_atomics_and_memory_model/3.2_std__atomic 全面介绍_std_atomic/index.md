# 3.2 std::atomic 全面介绍  std atomic

掌握 C++ 原子类型、操作、约束与工程用法。

## 本节目录

- [3.2.1 std::atomic<T> 的基本语义  atomic template basics](3.2.1_std__atomic_T_%20的基本语义_atomic_template_basics/index.md)
- [3.2.2 load、store 与 exchange  load store exchange](3.2.2_load、store%20与%20exchange_load_store_exchange/index.md)
- [3.2.3 fetch_add、fetch_sub 与复合操作  fetch operations](3.2.3_fetch_add、fetch_sub%20与复合操作_fetch_operations/index.md)
- [3.2.4 compare_exchange_weak 与 compare  exchange strong compare exchange weak and strong](3.2.4_compare_exchange_weak%20与%20compare_exchange_strong_compare_exchange_weak_and_strong/index.md)
- [3.2.5 std::atomic  flag atomic flag](3.2.5_std__atomic_flag_atomic_flag/index.md)
- [3.2.6 std::atomic<T*> 与指针原子操作  atomic pointer](3.2.6_std__atomic_T__%20与指针原子操作_atomic_pointer/index.md)
- [3.2.7 std::atomic  ref atomic ref](3.2.7_std__atomic_ref_atomic_ref/index.md)
- [3.2.8 is_lock_free 与 is  always lock free lock free queries](3.2.8_is_lock_free%20与%20is_always_lock_free_lock_free_queries/index.md)

---

## 导航

← 上一节：[3.1 C++ 并发内存模型  cpp concurrency memory model](../3.1_C++%20并发内存模型_cpp_concurrency_memory_model/index.md)
↑ 返回上级：[3 C++ 原子库与内存模型  cpp atomics and memory model](../index.md)
下一节：[3.3 Memory Order 六种内存序  memory order](../3.3_Memory%20Order%20六种内存序_memory_order/index.md) →
