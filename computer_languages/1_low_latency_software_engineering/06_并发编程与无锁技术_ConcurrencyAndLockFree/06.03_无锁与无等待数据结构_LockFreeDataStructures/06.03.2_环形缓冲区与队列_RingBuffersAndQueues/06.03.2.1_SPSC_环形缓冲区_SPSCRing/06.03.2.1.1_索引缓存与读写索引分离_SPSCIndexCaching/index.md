# 6.3.2.1.1 索引缓存与读写索引分离

缓存对端索引以减少跨核缓存行传输。

## 本节目录

- [6.3.2.1.1.1 cached_head 的刷新时机](06.03.2.1.1.1_cached_head_的刷新时机_CachedHeadRefresh/index.md)
- [6.3.2.1.1.2 对端索引读取的批量化](06.03.2.1.1.2_对端索引读取的批量化_PeerIndexBatching/index.md)

---

## 导航

← 上一节：[6.3.1 无锁进度保证](../../../06.03.1_无锁进度保证_ProgressGuarantees/index.md)
↑ 返回上级：[6.3.2.1 SPSC 环形缓冲区](../index.md)
下一节：[6.3.2.1.2 批量读写与零拷贝预留提交](../06.03.2.1.2_批量读写与零拷贝预留提交_SPSCBatchReserve/index.md) →
