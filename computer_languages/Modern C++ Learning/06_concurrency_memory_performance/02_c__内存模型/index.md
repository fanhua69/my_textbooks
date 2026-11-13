# 6.2 C++ 内存模型

理解并发访问规则、数据竞争和 happens-before 关系。

## 本节目录

- [6.2.1 数据竞争 Data Race 与未定义行为](01_数据竞争_data_race_与未定义行为/index.md)
- [6.2.2 原子操作与 std::atomic](02_原子操作与_std_atomic/index.md)
- [6.2.3 memory_order：relaxed 到 seq_cst](03_memory_order_relaxed_到_seq_cst/index.md)
- [6.2.4 happens-before 与 synchronizes-with](04_happens_before_与_synchronizes_with/index.md)
- [6.2.5 编译器重排、CPU 重排与 as-if rule](05_编译器重排_cpu_重排与_as_if_rule/index.md)

---

## 导航

← 上一节：[6.1.5 future、promise、async 与 packaged_task](../01_线程与同步原语/05_future_promise_async_与_packaged_task/index.md)
下一节：[6.2.1 数据竞争 Data Race 与未定义行为](01_数据竞争_data_race_与未定义行为/index.md) →
