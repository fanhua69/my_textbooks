# 01 syscall / svc / int 陷入路径与寄存器/栈切换

**介绍**: 追踪用户态到内核态的特权级跃迁、内核栈切换及返回路径上的微架构开销。

---

## 导航

← 上一节：[2.1.1 宏内核（Linux）、混合内核（XNU / Windows NT）与微内核对比](../../01_宏内核_linux_混合内核_xnu_windows_nt_与微内核对比/index.md)
↑ 返回上级：[2.1.2 中断、异常、陷入与上下文保存/恢复开销](../index.md)
下一节：[2.1.2.2 KPTI 页表切换与 Spectre/Meltdown 缓解对延迟的影响](../02_kpti_页表切换与_spectre_meltdown_缓解对延迟的影响/index.md) →
