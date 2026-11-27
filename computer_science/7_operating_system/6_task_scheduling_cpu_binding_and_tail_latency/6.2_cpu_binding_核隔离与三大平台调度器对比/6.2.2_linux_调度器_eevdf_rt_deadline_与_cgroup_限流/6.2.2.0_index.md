# 6.2.2 Linux 调度器（EEVDF / CFS / RT / Deadline）与 cgroup cpu.max 限流

**介绍**: 重点剖析 cgroup cpu.max 周期性限流引发的突发性几十毫秒延迟毛刺及规避方案。

## 目录

- [6.2.2.1 EEVDF / CFS 调度行为与 SCHED FIFO / SCHED DEADLINE 配置](6.2.2.1_eevdf_cfs_调度行为与实时调度配置/index.md)
- [6.2.2.2 cgroup v2 cpu.max 限流尖峰与低延迟部署规范](6.2.2.2_cgroup_v2_cpu_max_限流尖峰与低延迟部署规范/index.md)

## 导航

← 上一节：[6.2.1 CPU Binding 策略：物理核映射、避开超线程争用与 NUMA 协同绑核](../6.2.1_cpu_binding_策略_物理核映射与_numa_协同/index.md)
↑ 返回上级：[6.2 CPU Binding（绑核）、核隔离与三大平台调度器对比](../index.md)
下一节：[6.2.3 macOS GCD / QoS 与 Windows 线程优先级 / 组调度 / EcoQoS](../6.2.3_macos_gcd_qos_与_windows_调度器特性/index.md) →
