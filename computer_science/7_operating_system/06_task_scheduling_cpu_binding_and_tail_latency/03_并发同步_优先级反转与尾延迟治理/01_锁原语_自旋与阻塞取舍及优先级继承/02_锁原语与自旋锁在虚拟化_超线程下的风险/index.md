# 6.3.1.2 互斥锁、读写锁与自旋锁在虚拟化/超线程下的风险

识别锁持有者被抢占或 vCPU 被调度出去时自旋等待造成的空转浪费与延迟抖动。

---

## 导航

← 上一节：[6.3.1.1 优先级反转成因、Priority Inheritance 与 Priority Ceiling](../01_优先级反转成因_priority_inheritance_与_priority_ceiling/index.md)
↑ 返回上级：[6.3.1 锁原语、自旋与阻塞取舍及优先级继承](../index.md)
下一节：[6.3.2 热路径纪律与 P50 / P99 / P99.9 / P99.99 尾延迟治理闭环](../../02_热路径纪律与尾延迟治理闭环/index.md) →
