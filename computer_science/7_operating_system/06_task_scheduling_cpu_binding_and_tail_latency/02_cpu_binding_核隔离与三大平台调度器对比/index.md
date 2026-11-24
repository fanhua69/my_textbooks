# 02 CPU Binding（绑核）、核隔离与三大平台调度器对比

**介绍**: 掌握 CPU Affinity 绑核设计、隔离核规划与 Linux、macOS、Windows 调度器控制接口及典型毛刺。

## 目录

- [01 CPU Binding 策略：物理核映射、避开超线程争用与 NUMA 协同绑核](01_cpu_binding_策略_物理核映射与_numa_协同/index.md)
- [02 Linux 调度器（EEVDF / CFS / RT / Deadline）与 cgroup cpu.max 限流](02_linux_调度器_eevdf_rt_deadline_与_cgroup_限流/index.md)
- [03 macOS GCD / QoS 与 Windows 线程优先级 / 组调度 / EcoQoS](03_macos_gcd_qos_与_windows_调度器特性/index.md)

## 导航

← 上一节：[6.1 多核任务调度器核心机制与切换开销](../01_多核任务调度器核心机制与切换开销/index.md)
↑ 返回上级：[6 任务调度、CPU Binding 与尾延迟（P99 / P99.9）治理](../index.md)
下一节：[6.3 并发同步、优先级反转与尾延迟（P99 / P99.9 / P99.99）治理](../03_并发同步_优先级反转与尾延迟治理/index.md) →
