# 2.1.2 中断、异常、陷入与上下文保存/恢复开销

剖析寄存器保存/恢复、内核栈切换、页表隔离（KPTI）与预测执行缓解带来的纳秒级抖动。

## 本节目录

- [2.1.2.1 syscall / svc / int 陷入路径与寄存器/栈切换](01_syscall_svc_int_陷入路径与寄存器_栈切换/index.md)
- [2.1.2.2 KPTI 页表切换与 Spectre/Meltdown 缓解对延迟的影响](02_kpti_页表切换与_spectre_meltdown_缓解对延迟的影响/index.md)

---

## 导航

← 上一节：[2.1.1 宏内核（Linux）、混合内核（XNU / Windows NT）与微内核对比](../01_宏内核_linux_混合内核_xnu_windows_nt_与微内核对比/index.md)
↑ 返回上级：[2.1 内核架构、陷入开销与系统调用路径](../index.md)
下一节：[2.1.3 系统调用批处理、io uring 与内核态/用户态边界跨越优化](../03_系统调用批处理_io_uring_与边界跨越优化/index.md) →
