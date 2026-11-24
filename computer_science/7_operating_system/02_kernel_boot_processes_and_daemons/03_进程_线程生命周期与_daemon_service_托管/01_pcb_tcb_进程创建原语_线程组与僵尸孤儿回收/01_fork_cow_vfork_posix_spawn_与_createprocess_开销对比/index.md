# 2.3.1.1 fork/COW、vfork、posix spawn 与 CreateProcess 开销对比

剖析大内存进程 fork 页表复制与 TLB 刷新代价，以及 posix_spawn/CreateProcess 的工程优势。

---

## 导航

← 上一节：[2.2 系统启动流程（Boot）与早期初始化](../../../02_系统启动流程_boot_与早期初始化/index.md)
↑ 返回上级：[2.3.1 PCB/TCB、fork/vfork/posix spawn/CreateProcess、线程组与僵尸/孤儿回收](../index.md)
下一节：[2.3.1.2 进程组、会话、控制终端与僵尸/孤儿进程回收](../02_进程组_会话_控制终端与僵尸_孤儿进程回收/index.md) →
