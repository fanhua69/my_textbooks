# 2.3.1.2 进程组、会话、控制终端与僵尸/孤儿进程回收

掌握 SIGCHLD 处理、waitpid 非阻塞回收、subreaper 与 PID 1 托管孤儿进程的机制。

---

## 导航

← 上一节：[2.3.1.1 fork/COW、vfork、posix spawn 与 CreateProcess 开销对比](../01_fork_cow_vfork_posix_spawn_与_createprocess_开销对比/index.md)
↑ 返回上级：[2.3.1 PCB/TCB、fork/vfork/posix spawn/CreateProcess、线程组与僵尸/孤儿回收](../index.md)
下一节：[2.3.2 Linux systemd Unit（.service/.socket/.slice）、cgroup v2 追踪与资源限额](../../02_linux_systemd_unit_cgroup_v2_与资源限额/index.md) →
