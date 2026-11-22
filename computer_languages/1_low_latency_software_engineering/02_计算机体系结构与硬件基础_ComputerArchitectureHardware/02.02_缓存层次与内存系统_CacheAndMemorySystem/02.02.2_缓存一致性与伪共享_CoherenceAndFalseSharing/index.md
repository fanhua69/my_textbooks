# 2.2.2 缓存一致性与伪共享

多核写共享引发的缓存行乒乓是最常见的并发性能杀手。

## 本节目录

- [2.2.2.1 MESI 与 MOESI 协议](02.02.2.1_MESI_与_MOESI_协议_MESIProtocols/index.md)
- [2.2.2.2 伪共享的识别与消除](02.02.2.2_伪共享的识别与消除_FalseSharing/index.md)
- [2.2.2.3 真共享与热点缓存行](02.02.2.3_真共享与热点缓存行_TrueSharing/index.md)
- [2.2.2.4 缓存行对齐与 destructive interference size](02.02.2.4_缓存行对齐与_destructive_interference_size_CacheLineAlignment/index.md)

---

## 导航

← 上一节：[2.2.1 缓存结构与替换策略](../02.02.1_缓存结构与替换策略_CacheOrganization/index.md)
↑ 返回上级：[2.2 缓存层次与内存系统](../index.md)
下一节：[2.2.3 预取与内存级并行](../02.02.3_预取与内存级并行_PrefetchAndMLP/index.md) →
