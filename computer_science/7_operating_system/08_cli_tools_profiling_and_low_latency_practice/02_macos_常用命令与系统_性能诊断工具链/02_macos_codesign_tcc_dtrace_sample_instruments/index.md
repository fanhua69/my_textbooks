# 02 代码签名、TCC/权限与剖析工具：codesign、spctl、security、tccutil、lsof、dtrace / sample / spindump / Instruments

**介绍**: 校验签名与权限需求、排查文件/端口占用，结合 Instruments 与 dtrace/sample/spindump 定位延迟与阻塞。

## 目录

- [01 codesign、spctl、security、tccutil 与 lsof 签名/权限/句柄排查](01_codesign_spctl_security_tccutil_与_lsof_用法/index.md)
- [02 Instruments（Time Profiler / System Trace / Allocations）与 sample / spindump / dtrace](02_instruments_与_sample_spindump_dtrace_剖析/index.md)

## 导航

← 上一节：[8.2.1 服务、进程、内存与日志命令：launchctl、ps、top、vm stat、memory pressure、log、sysctl](../01_macos_launchctl_内存压力_统一日志与内核参数/index.md)
↑ 返回上级：[8.2 macOS 常用命令与系统/性能诊断工具链](../index.md)
下一节：[8.3 Windows 常用命令与系统/性能诊断工具链](../../03_windows_常用命令与系统_性能诊断工具链/index.md) →
