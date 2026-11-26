# 6.2.1.2 隔离核（isolcpus / nohz full / cpuset）与系统后台线程隔离

**介绍**: 将内核工作线程、监控探针与无关业务移出专用低延迟核心集合。

---

## 导航

← 上一节：[6.2.1.1 线程绑核接口、物理核/SMT 拓扑识别与专职线程划分](../6.2.1.1_线程绑核接口与物理核_smt_拓扑识别/index.md)
↑ 返回上级：[6.2.1 CPU Binding 策略：物理核映射、避开超线程争用与 NUMA 协同绑核](../index.md)
下一节：[6.2.2 Linux 调度器（EEVDF / CFS / RT / Deadline）与 cgroup cpu.max 限流](../../6.2.2_linux_调度器_eevdf_rt_deadline_与_cgroup_限流/index.md) →
