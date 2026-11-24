# 2.3.3 大页内存（HugeTLB / THP）与 NUMA 亲和性优化

**介绍**: 降低高频交易与高性能计算场景下共享内存的 TLB Miss 与跨 NUMA 节点访问延迟。

---

## 导航

← 上一节：[2.3.2 匿名内存文件 memfd create 与文件封印（File Sealing）](../2.3.2_匿名内存文件_memfd_create_与文件封印_file_sealing/index.md)
↑ 返回上级：[2.3 共享内存与内存文件描述符](../index.md)
下一节：[2.4 现代内核事件通知与消息总线](../../2.4_现代内核事件通知与消息总线/index.md) →
