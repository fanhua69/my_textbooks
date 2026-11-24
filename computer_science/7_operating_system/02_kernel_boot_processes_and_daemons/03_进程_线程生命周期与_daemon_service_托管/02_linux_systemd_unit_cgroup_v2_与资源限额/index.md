# 02 Linux systemd Unit（.service/.socket/.slice）、cgroup v2 追踪与资源限额

**介绍**: 掌握启动类型、Socket 激活、cgroup 进程树精确追踪及 CPU/内存/PIDs 限额对延迟的影响。

## 目录

- [01 .service 启动类型、sd notify 就绪通知与 Socket Activation](01_service_启动类型_sd_notify_就绪通知与_socket_activation/index.md)
- [02 cgroup v2 进程组追踪、cpu.max 限流与内存/PIDs 保护](02_cgroup_v2_进程组追踪_cpu_max_限流与内存_pids_保护/index.md)

## 导航

← 上一节：[2.3.1 PCB/TCB、fork/vfork/posix spawn/CreateProcess、线程组与僵尸/孤儿回收](../01_pcb_tcb_进程创建原语_线程组与僵尸孤儿回收/index.md)
↑ 返回上级：[2.3 进程、线程生命周期与 Daemon / Service 托管](../index.md)
下一节：[2.3.3 macOS LaunchDaemon、LaunchAgent、领域（Domain）与按需激活（On-Demand）](../03_macos_launchdaemon_launchagent_领域与按需激活/index.md) →
