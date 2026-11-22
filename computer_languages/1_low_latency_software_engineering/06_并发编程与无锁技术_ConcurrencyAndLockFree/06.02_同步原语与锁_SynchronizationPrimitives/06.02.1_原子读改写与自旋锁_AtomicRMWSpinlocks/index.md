# 6.2.1 原子读改写与自旋锁

最小开销的互斥实现。

## 本节目录

- [6.2.1.1 CAS、LL/SC 与 fetch_add](06.02.1.1_CAS_LL_SC_与_fetch_add_CASLLSC/index.md)
- [6.2.1.2 自旋锁、TTAS 与退避](06.02.1.2_自旋锁_TTAS_与退避_SpinlocksBackoff/index.md)
- [6.2.1.3 公平自旋锁：Ticket、MCS 与 CLH](06.02.1.3_公平自旋锁_Ticket_MCS_与_CLH_TicketMCSCLH/index.md)

---

## 导航

← 上一节：[6.1 内存模型与有序性](../../06.01_内存模型与有序性_MemoryModels/index.md)
↑ 返回上级：[6.2 同步原语与锁](../index.md)
下一节：[6.2.2 内核辅助的锁](../06.02.2_内核辅助的锁_KernelAssistedLocks/index.md) →
