# 2.2.7.4 存储缓冲区与存储转发

理解存储缓冲区如何产生重排，以及对延迟与无锁算法的影响。

## 本节目录

- [2.2.7.4.1 存储缓冲区与 StoreLoad 重排](02.02.7.4.1_存储缓冲区与_StoreLoad_重排_StoreBufferStoreLoad/index.md)
- [2.2.7.4.2 存储到加载转发](02.02.7.4.2_存储到加载转发_StoreToLoadForwarding/index.md)
- [2.2.7.4.3 内存歧义消除与推测加载](02.02.7.4.3_内存歧义消除与推测加载_MemoryDisambiguation/index.md)
- [2.2.7.4.4 写合并缓冲与存储合并](02.02.7.4.4_写合并缓冲与存储合并_WriteCombiningStoreMerging/index.md)

---

## 导航

← 上一节：[2.2.7.3 非时间存储与写合并](../02.02.7.3_非时间存储与写合并_NonTemporalAndWC/index.md)
↑ 返回上级：[2.2.7 内存模型与有序性](../index.md)
下一节：[2.3 向量化与数据级并行](../../../02.03_向量化与数据级并行_SIMDAndDataParallelism/index.md) →
