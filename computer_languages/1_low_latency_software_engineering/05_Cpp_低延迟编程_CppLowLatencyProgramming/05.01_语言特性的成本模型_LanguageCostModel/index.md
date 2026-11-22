# 5.1 语言特性的成本模型

逐一评估 C++ 各特性在热路径上的真实开销，建立“零成本抽象”的批判性认识。

## 本节目录

- [5.1.1 调用与分发机制](05.01.1_调用与分发机制_CallAndDispatch/index.md)
- [5.1.2 异常、RTTI 与运行时设施](05.01.2_异常_RTTI_与运行时设施_ExceptionsRTTI/index.md)
- [5.1.3 构造、拷贝与移动](05.01.3_构造_拷贝与移动_ObjectLifecycleCost/index.md)
- [5.1.4 模板与代码膨胀](05.01.4_模板与代码膨胀_TemplatesAndBloat/index.md)

---

## 导航

← 上一节：[4 网络与通信延迟工程](../../04_网络与通信延迟工程_NetworkAndCommunicationLatency/index.md)
↑ 返回上级：[5 C++ 低延迟编程](../index.md)
下一节：[5.2 内存管理与分配器](../05.02_内存管理与分配器_MemoryAllocators/index.md) →
