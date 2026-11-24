# 2.3.2.1 .service 启动类型、sd notify 就绪通知与 Socket Activation

**介绍**: 避免将未就绪服务视为已启动，使用 Socket 激活实现零丢连按需拉起与平滑重启。

---

## 导航

← 上一节：[2.3.1 PCB/TCB、fork/vfork/posix spawn/CreateProcess、线程组与僵尸/孤儿回收](../../2.3.1_pcb_tcb_进程创建原语_线程组与僵尸孤儿回收/index.md)
↑ 返回上级：[2.3.2 Linux systemd Unit（.service/.socket/.slice）、cgroup v2 追踪与资源限额](../index.md)
下一节：[2.3.2.2 cgroup v2 进程组追踪、cpu.max 限流与内存/PIDs 保护](../2.3.2.2_cgroup_v2_进程组追踪_cpu_max_限流与内存_pids_保护/index.md) →
