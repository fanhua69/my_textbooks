# 2.3.1 PCB/TCB、fork/vfork/posix spawn/CreateProcess、线程组与僵尸/孤儿回收

对比 fork 页表复制开销与 posix_spawn 轻量创建、进程组/会话控制终端以及 waitpid/信号回收语义。

## 本节目录

- [2.3.1.1 fork/COW、vfork、posix spawn 与 CreateProcess 开销对比](01_fork_cow_vfork_posix_spawn_与_createprocess_开销对比/index.md)
- [2.3.1.2 进程组、会话、控制终端与僵尸/孤儿进程回收](02_进程组_会话_控制终端与僵尸_孤儿进程回收/index.md)

---

## 导航

← 上一节：[2.2 系统启动流程（Boot）与早期初始化](../../02_系统启动流程_boot_与早期初始化/index.md)
↑ 返回上级：[2.3 进程、线程生命周期与 Daemon / Service 托管](../index.md)
下一节：[2.3.2 Linux systemd Unit（.service/.socket/.slice）、cgroup v2 追踪与资源限额](../02_linux_systemd_unit_cgroup_v2_与资源限额/index.md) →
