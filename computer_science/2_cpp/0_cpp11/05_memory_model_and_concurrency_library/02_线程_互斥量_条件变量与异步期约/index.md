# 5.2 <thread>、<mutex>、<condition variable> 与 <future>

掌握标准库线程管理、死锁安全加锁原语、条件等待及异步任务结果传递。

## 本节目录

- [5.2.1 std::thread 线程创建、join / detach 与 std::this thread 工具](01_std_thread_与_this_thread/index.md)
- [5.2.2 std::mutex、recursive_mutex、timed_mutex、lock_guard、unique_lock、std::lock 与 std::call  once](02_互斥量_lock_guard_unique_lock_与_call_once/index.md)
- [5.2.3 std::condition_variable 与 std::condition  variable any](03_condition_variable_与等待谓词/index.md)
- [5.2.4 std::promise、std::future、std::shared future、std::packaged task 与 std::async](04_promise_future_packaged_task_与_async/index.md)

---

## 导航

← 上一节：[5.1 C++11 内存模型、数据竞争与 std::thread  local](../01_内存模型_数据竞争与_thread_local/index.md)
↑ 返回上级：[5 C++11 内存模型、并发与原子支持库](../index.md)
下一节：[5.3 <atomic> 原子操作、内存序（memory order）与栅栏](../03_atomic_原子操作_内存序与栅栏/index.md) →
