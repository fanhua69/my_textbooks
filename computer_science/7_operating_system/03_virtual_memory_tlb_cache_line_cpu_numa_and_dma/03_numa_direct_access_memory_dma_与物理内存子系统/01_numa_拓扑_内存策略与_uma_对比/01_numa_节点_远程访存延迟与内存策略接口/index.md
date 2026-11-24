# 01 NUMA 节点、本地 vs 远程内存访问延迟与 numactl / mbind / set  mempolicy

**介绍**: 避免跨 NUMA 节点频繁读写导致的延迟上升，掌握线程与内存本地化配置方法。

---

## 导航

← 上一节：[3.2 CPU 架构、Cache Line 层次与缓存一致性协议](../../../02_cpu_架构_cache_line_层次与缓存一致性协议/index.md)
↑ 返回上级：[3.3.1 NUMA 节点拓扑、跨节点访存延迟、内存策略与 macOS UMA 对比](../index.md)
下一节：[3.3.1.2 Linux NUMA、macOS 统一内存（UMA）与 Windows 内存节点/工作集对比](../02_三平台_numa_uma_与内存节点特性对比/index.md) →
