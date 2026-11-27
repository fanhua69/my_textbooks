# 6.1.4 内存回收与 ABA 的关系  reclamation and aba

**介绍**: 理解安全回收如何降低地址复用导致的 ABA 风险。

---

## 导航

← 上一节：[6.1.3 为什么不能直接 delete 节点  why direct delete is unsafe](../6.1.3_%E4%B8%BA%E4%BB%80%E4%B9%88%E4%B8%8D%E8%83%BD%E7%9B%B4%E6%8E%A5%20delete%20%E8%8A%82%E7%82%B9_why_direct_delete_is_unsafe/index.md)
↑ 返回上级：[6.1 无锁数据结构的内存生命周期问题  memory lifetime problems](../index.md)
下一节：[6.1.5 节点生命周期与所有权协议  node lifetime and ownership protocol](../6.1.5_节点生命周期与所有权协议_node_lifetime_and_ownership_protocol/index.md) →
