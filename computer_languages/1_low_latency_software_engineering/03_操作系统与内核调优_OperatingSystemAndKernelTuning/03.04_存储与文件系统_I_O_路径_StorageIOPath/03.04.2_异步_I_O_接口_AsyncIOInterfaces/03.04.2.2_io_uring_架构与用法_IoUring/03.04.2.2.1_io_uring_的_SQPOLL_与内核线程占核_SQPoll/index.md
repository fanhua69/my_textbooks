# 3.4.2.2.1 io_uring 的 SQPOLL 与内核线程占核

免系统调用提交与专用核开销。

## 本节目录

- [3.4.2.2.1.1 sq_thread_idle 与空闲让出](03.04.2.2.1.1_sq_thread_idle_与空闲让出_SqThreadIdle/index.md)
- [3.4.2.2.1.2 SQPOLL 线程与应用线程的核分配](03.04.2.2.1.2_SQPOLL_线程与应用线程的核分配_SqPollCoreAllocation/index.md)

---

## 导航

← 上一节：[3.4.2.1 Linux AIO 的局限](../../03.04.2.1_Linux_AIO_的局限_LinuxAIOLimits/index.md)
↑ 返回上级：[3.4.2.2 io_uring 架构与用法](../index.md)
下一节：[3.4.2.2.2 io_uring 网络与零拷贝发送](../03.04.2.2.2_io_uring_网络与零拷贝发送_IoUringNetworking/index.md) →
