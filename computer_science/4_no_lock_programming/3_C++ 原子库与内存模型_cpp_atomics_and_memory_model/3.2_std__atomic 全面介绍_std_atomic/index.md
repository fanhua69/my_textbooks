# 3.2 std::atomic 全面介绍  std atomic

**介绍**: 掌握 C++ 原子类型、操作、约束与工程用法。

## 目录

- [3.2.1 std::atomic<T> 的基本语义  atomic template basics](3.2.1_std__atomic_T_%20%E7%9A%84%E5%9F%BA%E6%9C%AC%E8%AF%AD%E4%B9%89_atomic_template_basics/index.md)
- [3.2.2 load、store 与 exchange  load store exchange](3.2.2_load%E3%80%81store%20%E4%B8%8E%20exchange_load_store_exchange/index.md)
- [3.2.3 fetch_add、fetch_sub 与复合操作  fetch operations](3.2.3_fetch_add%E3%80%81fetch_sub%20%E4%B8%8E%E5%A4%8D%E5%90%88%E6%93%8D%E4%BD%9C_fetch_operations/index.md)
- [3.2.4 compare_exchange_weak 与 compare  exchange strong compare exchange weak and strong](3.2.4_compare_exchange_weak%20%E4%B8%8E%20compare_exchange_strong_compare_exchange_weak_and_strong/index.md)
- [3.2.5 std::atomic  flag atomic flag](3.2.5_std__atomic_flag_atomic_flag/index.md)
- [3.2.6 std::atomic<T*> 与指针原子操作  atomic pointer](3.2.6_std__atomic_T__%20%E4%B8%8E%E6%8C%87%E9%92%88%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C_atomic_pointer/index.md)
- [3.2.7 std::atomic  ref atomic ref](3.2.7_std__atomic_ref_atomic_ref/index.md)
- [3.2.8 is_lock_free 与 is  always lock free lock free queries](3.2.8_is_lock_free%20%E4%B8%8E%20is_always_lock_free_lock_free_queries/index.md)

## 导航

← 上一节：[3.1 C++ 并发内存模型  cpp concurrency memory model](../3.1_C++%20并发内存模型_cpp_concurrency_memory_model/index.md)
↑ 返回上级：[3 C++ 原子库与内存模型  cpp atomics and memory model](../index.md)
下一节：[3.3 Memory Order 六种内存序  memory order](../3.3_Memory%20Order%20六种内存序_memory_order/index.md) →
