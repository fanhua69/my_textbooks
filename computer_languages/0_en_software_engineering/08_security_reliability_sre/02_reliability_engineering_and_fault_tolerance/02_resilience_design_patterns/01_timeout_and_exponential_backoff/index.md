# 8.2.2.1 超时机制与带抖动的指数退避重试

严格设置各级 RPC 调用超时，重试必须叠加 Exponential Backoff 与 Jitter 随机抖动以避免造成后端重试风暴。

---

## 导航

← 上一节：[8.2.1 高可用架构设计与容灾](../../01_high_availability_architectures/index.md)
↑ 返回上级：[8.2.2 弹性设计核心模式](../index.md)
下一节：[8.2.2.2 断路器模式 (Circuit Breaker) 状态机演化](../02_circuit_breaker_pattern/index.md) →
