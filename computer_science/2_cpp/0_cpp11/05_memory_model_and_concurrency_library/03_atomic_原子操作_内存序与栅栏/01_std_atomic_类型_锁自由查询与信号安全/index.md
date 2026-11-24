# 5.3.1 std::atomic<T>、特化接口、is lock free 与信号处理器安全

掌握 load、store、exchange、compare_exchange_weak / compare_exchange_strong、fetch_add/sub/and/or/xor 及 is_lock_free()。

---

## 导航

← 上一节：[5.2 <thread>、<mutex>、<condition variable> 与 <future>](../../02_线程_互斥量_条件变量与异步期约/index.md)
↑ 返回上级：[5.3 <atomic> 原子操作、内存序（memory order）与栅栏](../index.md)
下一节：[5.3.2 memory order（relaxed、consume、acquire、release、acq rel、seq cst）与原子栅栏](../02_memory_order_语义与原子栅栏/index.md) →
