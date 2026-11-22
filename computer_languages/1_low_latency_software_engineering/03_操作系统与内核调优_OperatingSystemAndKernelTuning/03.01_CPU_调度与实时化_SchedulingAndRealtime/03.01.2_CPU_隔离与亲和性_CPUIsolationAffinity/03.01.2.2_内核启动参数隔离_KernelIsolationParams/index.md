# 3.1.2.2 内核启动参数隔离

isolcpus、nohz_full、rcu_nocbs 与 irqaffinity 的协同配置。

## 本节目录

- [3.1.2.2.1 isolcpus 与 cpuset 的取舍](03.01.2.2.1_isolcpus_与_cpuset_的取舍_IsolcpusVsCpuset/index.md)
- [3.1.2.2.2 无时钟滴答模式 nohz_full](03.01.2.2.2_无时钟滴答模式_nohz_full_NoHzFull/index.md)
- [3.1.2.2.3 RCU 回调卸载](03.01.2.2.3_RCU_回调卸载_RCUOffload/index.md)

---

## 导航

← 上一节：[3.1.2.1 线程绑核与亲和性 API](../03.01.2.1_线程绑核与亲和性_API_AffinityAPIs/index.md)
↑ 返回上级：[3.1.2 CPU 隔离与亲和性](../index.md)
下一节：[3.1.2.3 线程放置策略](../03.01.2.3_线程放置策略_ThreadPlacement/index.md) →
