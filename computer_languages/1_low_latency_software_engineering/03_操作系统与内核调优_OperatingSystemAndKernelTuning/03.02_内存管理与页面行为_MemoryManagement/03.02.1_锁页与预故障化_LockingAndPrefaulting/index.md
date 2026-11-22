# 3.2.1 锁页与预故障化

让关键内存永远驻留物理页并提前完成映射。

## 本节目录

- [3.2.1.1 mlock、mlockall 与 RLIMIT_MEMLOCK](03.02.1.1_mlock_mlockall_与_RLIMIT_MEMLOCK_MlockFamily/index.md)
- [3.2.1.2 启动期预触碰与堆预热](03.02.1.2_启动期预触碰与堆预热_PretouchWarmup/index.md)
- [3.2.1.3 关闭 overcommit 与 swap](03.02.1.3_关闭_overcommit_与_swap_DisableSwapOvercommit/index.md)

---

## 导航

← 上一节：[3.1 CPU 调度与实时化](../../03.01_CPU_调度与实时化_SchedulingAndRealtime/index.md)
↑ 返回上级：[3.2 内存管理与页面行为](../index.md)
下一节：[3.2.2 大页与内存策略](../03.02.2_大页与内存策略_HugePagePolicies/index.md) →
