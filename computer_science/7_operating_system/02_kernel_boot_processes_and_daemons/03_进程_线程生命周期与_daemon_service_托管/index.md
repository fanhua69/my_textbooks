# 2.3 进程、线程生命周期与 Daemon / Service 托管

深入进程/线程控制块、地址空间克隆与后台守护进程管理机制，防范僵尸进程、孤儿进程与启动/重启抖动。

## 本节目录

- [2.3.1 PCB/TCB、fork/vfork/posix spawn/CreateProcess、线程组与僵尸/孤儿回收](01_pcb_tcb_进程创建原语_线程组与僵尸孤儿回收/index.md)
- [2.3.2 Linux systemd Unit（.service/.socket/.slice）、cgroup v2 追踪与资源限额](02_linux_systemd_unit_cgroup_v2_与资源限额/index.md)
- [2.3.3 macOS LaunchDaemon、LaunchAgent、领域（Domain）与按需激活（On-Demand）](03_macos_launchdaemon_launchagent_领域与按需激活/index.md)
- [2.3.4 Windows Service、SCM 状态机、Session 0 隔离与服务恢复策略](04_windows_service_scm_状态机_session0_隔离与服务恢复策略/index.md)

---

## 导航

← 上一节：[2.2 系统启动流程（Boot）与早期初始化](../02_系统启动流程_boot_与早期初始化/index.md)
↑ 返回上级：[2 内核架构、启动链路、进程与 Daemon/Service 托管](../index.md)
下一节：[3 虚拟内存、TLB、Cache Line、CPU、NUMA、DMA 与硬件内存体系](../../03_virtual_memory_tlb_cache_line_cpu_numa_and_dma/index.md) →
