# 01 CPU Binding 策略：物理核映射、避开超线程争用与 NUMA 协同绑核

**介绍**: 掌握线程与特定 CPU 核心绑定（pthread_setaffinity_np / sched_setaffinity / SetThreadAffinityMask）及避免跨 NUMA 绑核。

## 目录

- [01 线程绑核接口、物理核/SMT 拓扑识别与专职线程划分](01_线程绑核接口与物理核_smt_拓扑识别/index.md)
- [02 隔离核（isolcpus / nohz full / cpuset）与系统后台线程隔离](02_隔离核配置与系统后台线程隔离/index.md)

## 导航

← 上一节：[6.1 多核任务调度器核心机制与切换开销](../../01_多核任务调度器核心机制与切换开销/index.md)
↑ 返回上级：[6.2 CPU Binding（绑核）、核隔离与三大平台调度器对比](../index.md)
下一节：[6.2.2 Linux 调度器（EEVDF / CFS / RT / Deadline）与 cgroup cpu.max 限流](../02_linux_调度器_eevdf_rt_deadline_与_cgroup_限流/index.md) →
