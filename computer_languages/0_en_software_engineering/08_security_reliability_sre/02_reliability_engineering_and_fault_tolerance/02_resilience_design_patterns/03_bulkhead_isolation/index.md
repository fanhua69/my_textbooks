# 8.2.2.3 舱壁隔离模式 (Bulkhead Isolation)

仿照轮船水密舱设计，通过独立线程池与信号量隔离不同业务通道，防止单一慢服务耗尽全系统资源。

---

## 导航

← 上一节：[8.2.2.2 断路器模式 (Circuit Breaker) 状态机演化](../02_circuit_breaker_pattern/index.md)
↑ 返回上级：[8.2.2 弹性设计核心模式](../index.md)
下一节：[8.2.2.4 限流算法与背压保护 (Rate Limiting)](../04_rate_limiting_and_backpressure/index.md) →
