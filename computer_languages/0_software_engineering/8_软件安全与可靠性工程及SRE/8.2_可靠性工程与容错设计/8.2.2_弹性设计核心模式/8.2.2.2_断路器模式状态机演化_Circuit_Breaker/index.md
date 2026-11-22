# 8.2.2.2 断路器模式 (Circuit Breaker) 状态机演化

详细剖析 Closed（闭合正常）、Open（打开熔断快速失败）与 Half-Open（半开试探恢复）三态流转机制与回退降级（Fallback）。

---

## 导航

← 上一节：[8.2.2.1 超时机制与带抖动的指数退避重试](../8.2.2.1_超时机制与带抖动的指数退避重试/index.md)
↑ 返回上级：[8.2.2 弹性设计核心模式](../index.md)
下一节：[8.2.2.3 舱壁隔离模式 (Bulkhead Isolation)](../8.2.2.3_舱壁隔离模式_Bulkhead_Isolation/index.md) →
