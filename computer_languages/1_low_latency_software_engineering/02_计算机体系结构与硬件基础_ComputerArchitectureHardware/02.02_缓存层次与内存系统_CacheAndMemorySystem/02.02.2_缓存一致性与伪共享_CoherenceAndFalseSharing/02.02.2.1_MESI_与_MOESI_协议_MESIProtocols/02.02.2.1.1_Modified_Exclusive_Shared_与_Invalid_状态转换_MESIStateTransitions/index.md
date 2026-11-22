# 2.2.2.1.1 Modified、Exclusive、Shared 与 Invalid 状态转换

读写操作如何驱动缓存行在四种状态间迁移。

## 本节目录

- [2.2.2.1.1.1 读未命中的嗅探响应路径](02.02.2.1.1.1_读未命中的嗅探响应路径_ReadMissSnoopPath/index.md)
- [2.2.2.1.1.2 写入时的 RFO 与失效广播](02.02.2.1.1.2_写入时的_RFO_与失效广播_RFOInvalidation/index.md)

---

## 导航

← 上一节：[2.2.1 缓存结构与替换策略](../../../02.02.1_缓存结构与替换策略_CacheOrganization/index.md)
↑ 返回上级：[2.2.2.1 MESI 与 MOESI 协议](../index.md)
下一节：[2.2.2.1.2 Forward 与 Owned 状态扩展](../02.02.2.1.2_Forward_与_Owned_状态扩展_ForwardOwnedStates/index.md) →
