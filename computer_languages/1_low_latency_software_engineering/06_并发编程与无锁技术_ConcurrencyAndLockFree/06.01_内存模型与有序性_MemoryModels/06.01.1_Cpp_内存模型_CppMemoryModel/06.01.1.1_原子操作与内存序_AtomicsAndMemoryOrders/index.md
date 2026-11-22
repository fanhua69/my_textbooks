# 6.1.1.1 原子操作与内存序

relaxed、acquire、release、acq_rel 与 seq_cst 的语义。

## 本节目录

- [6.1.1.1.1 acquire/release 配对与同步关系](06.01.1.1.1_acquire_release_配对与同步关系_AcquireReleasePairing/index.md)
- [6.1.1.1.2 seq_cst 的代价与全序](06.01.1.1.2_seq_cst_的代价与全序_SeqCstCost/index.md)
- [6.1.1.1.3 relaxed 的合法使用场景](06.01.1.1.3_relaxed_的合法使用场景_RelaxedUsage/index.md)
- [6.1.1.1.4 consume 的现状与替代](06.01.1.1.4_consume_的现状与替代_ConsumeStatus/index.md)

---

## 导航

← 上一节：[5 C++ 低延迟编程](../../../../05_Cpp_低延迟编程_CppLowLatencyProgramming/index.md)
↑ 返回上级：[6.1.1 C++ 内存模型](../index.md)
下一节：[6.1.1.2 数据竞争与未定义行为](../06.01.1.2_数据竞争与未定义行为_DataRaceUB/index.md) →
