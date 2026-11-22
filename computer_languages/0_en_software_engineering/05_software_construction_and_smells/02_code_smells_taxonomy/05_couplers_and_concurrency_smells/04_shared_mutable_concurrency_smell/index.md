# 5.2.5.4 并发共享可变状态异味

多线程中随意读写公共可变对象导致的竞态与死锁；改造为消息传递 Actor 模式或不可变快照。

---

## 导航

← 上一节：[5.2.5.3 过长消息链与中间人异味](../03_message_chains_and_middle_man/index.md)
↑ 返回上级：[5.2.5 耦合与并发类代码异味 (Couplers & Concurrency)](../index.md)
下一节：[5.3 设计异味与组件退化](../../../03_design_smells/index.md) →
