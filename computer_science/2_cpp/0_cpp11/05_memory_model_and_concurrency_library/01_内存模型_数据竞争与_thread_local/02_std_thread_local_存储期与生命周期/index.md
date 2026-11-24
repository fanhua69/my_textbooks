# 5.1.2 std::thread local 线程局部存储与构造/析构时机

掌握 thread_local 变量在块作用域、命名空间作用域与类静态成员中的初始化与线程退出时销毁规则。

---

## 导航

← 上一节：[5.1.1 内存位置、数据竞争（Data Race）、sequenced-before 与 happens-before](../01_内存位置_数据竞争与_happens_before/index.md)
↑ 返回上级：[5.1 C++11 内存模型、数据竞争与 std::thread  local](../index.md)
下一节：[5.2 <thread>、<mutex>、<condition variable> 与 <future>](../../02_线程_互斥量_条件变量与异步期约/index.md) →
