# 8.2.3.1 分布式幂等性实现方案

运用客户端全局唯一流水号（Idempotency Key）、防重 Token 机制与数据库唯一约束索引保证接口任意次调用的确定性结果。

---

## 导航

← 上一节：[8.2.2 弹性设计核心模式](../../02_resilience_design_patterns/index.md)
↑ 返回上级：[8.2.3 幂等性设计与防重放机制](../index.md)
下一节：[8.2.3.2 防重放攻击机制：时间戳与随机数 Nonce](../02_anti_replay_mechanisms/index.md) →
