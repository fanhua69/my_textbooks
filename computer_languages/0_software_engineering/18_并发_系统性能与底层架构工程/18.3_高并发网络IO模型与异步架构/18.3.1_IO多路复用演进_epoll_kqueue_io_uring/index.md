# 18.3.1 I/O 多路复用演进：select/poll、epoll/kqueue 与 io_uring

对比同步阻塞、非阻塞轮询、事件驱动多路复用以及现代 Linux 异步 I/O 引擎 io_uring 底层机制。

---

## 导航

← 上一节：[18.2 硬件亲和性 (Mechanical Sympathy)、内存模型与无锁并发](../../18.2_硬件亲和性_Mechanical_Sympathy_内存模型与无锁并发/index.md)
↑ 返回上级：[18.3 高并发网络 I/O 模型与异步架构](../index.md)
下一节：[18.3.2 Reactor 与 Proactor 高并发网络架构模式](../18.3.2_Reactor与Proactor高并发网络架构模式/index.md) →
