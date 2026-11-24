# 5.3 <atomic> 原子操作、内存序（memory order）与栅栏

掌握无锁原子类型、原子读改写原语、六种 memory_order 语义、信号处理器原子安全与内存栅栏。

## 本节目录

- [5.3.1 std::atomic<T>、特化接口、is lock free 与信号处理器安全](01_std_atomic_类型_锁自由查询与信号安全/index.md)
- [5.3.2 memory order（relaxed、consume、acquire、release、acq rel、seq cst）与原子栅栏](02_memory_order_语义与原子栅栏/index.md)

---

## 导航

← 上一节：[5.2 <thread>、<mutex>、<condition variable> 与 <future>](../02_线程_互斥量_条件变量与异步期约/index.md)
↑ 返回上级：[5 C++11 内存模型、并发与原子支持库](../index.md)
下一节：[6 C++11 标准库容器、智能指针、字符串、时间、正则与错误处理](../../06_cpp11_standard_library_components/index.md) →
