# 6.3.2.1.2 批量读写与零拷贝预留提交

先预留再提交的接口避免额外拷贝。

## 本节目录

- [6.3.2.1.2.1 reserve 与 commit 接口语义](06.03.2.1.2.1_reserve_与_commit_接口语义_ReserveCommitSemantics/index.md)
- [6.3.2.1.2.2 回绕处预留的处理](06.03.2.1.2.2_回绕处预留的处理_WrapAroundReserve/index.md)

---

## 导航

← 上一节：[6.3.2.1.1 索引缓存与读写索引分离](../06.03.2.1.1_索引缓存与读写索引分离_SPSCIndexCaching/index.md)
↑ 返回上级：[6.3.2.1 SPSC 环形缓冲区](../index.md)
下一节：[6.3.2.1.3 容量取 2 的幂与回绕处理](../06.03.2.1.3_容量取_2_的幂与回绕处理_SPSCPowerOfTwo/index.md) →
