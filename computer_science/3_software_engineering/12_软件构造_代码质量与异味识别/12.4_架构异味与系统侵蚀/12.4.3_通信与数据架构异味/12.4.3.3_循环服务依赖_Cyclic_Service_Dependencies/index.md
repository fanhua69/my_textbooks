# 12.4.3.3 循环服务依赖 (Cyclic Service Dependencies)

服务 A 调 B，B 调 C，C 又反向同步调 A；引发分布式死锁与级联雪崩；重构为异步事件驱动解耦。

---

## 导航

← 上一节：[12.4.3.2 共享数据库集成异味 (Shared Database Integration)](../12.4.3.2_共享数据库集成异味_Shared_Database_Integration/index.md)
↑ 返回上级：[12.4.3 通信与数据架构异味](../index.md)
下一节：[13 软件重构、技术债与软件演化](../../../../13_软件重构_技术债与软件演化/index.md) →
