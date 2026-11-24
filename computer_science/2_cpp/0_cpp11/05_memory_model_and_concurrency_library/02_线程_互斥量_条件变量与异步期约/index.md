# 5.2 线程、互斥量、条件变量与异步期约

掌握 std::thread、锁、条件变量与 future 体系，构建正确的并发程序。

## 本节目录

- [5.2.1 std::thread 的创建、传参与生命周期](01_std_thread_的创建_传参与生命周期/index.md)
- [5.2.2 this thread 与线程标识](02_this_thread_与线程标识/index.md)
- [5.2.3 互斥量与锁管理](03_互斥量与锁管理/index.md)
- [5.2.4 死锁与多锁获取：std::lock](04_死锁与多锁获取_std_lock/index.md)
- [5.2.5 条件变量与等待-通知模式](05_条件变量与等待_通知模式/index.md)
- [5.2.6 call once 与一次性初始化](06_call_once_与一次性初始化/index.md)
- [5.2.7 future、promise 与 packaged  task](07_future_promise_与_packaged_task/index.md)
- [5.2.8 std::async 与启动策略](08_std_async_与启动策略/index.md)
- [5.2.9 线程间异常传递与程序退出](09_线程间异常传递与程序退出/index.md)

---

## 导航

← 上一节：[5.1 内存模型、数据竞争与 thread  local](../01_内存模型_数据竞争与_thread_local/index.md)
↑ 返回上级：[5 内存模型与并发库](../index.md)
下一节：[5.3 atomic、原子操作、内存序与栅栏](../03_atomic_原子操作_内存序与栅栏/index.md) →
