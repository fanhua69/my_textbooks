# 2.2 系统启动流程（Boot）与早期初始化

**介绍**: 贯通固件、Bootloader、内核初始化与用户态一号进程拉起，识别启动阶段配置与安全校验点。

## 目录

- [2.2.1 固件引导（UEFI / iBoot）、Bootloader 与内核早期初始化](2.2.1_固件引导_uefi_iboot_bootloader_与早期初始化/index.md)
- [2.2.2 Linux 启动链：固件 -> Bootloader -> initramfs -> systemd（PID 1）](2.2.2_linux_启动链_initramfs_与_systemd_初始化/index.md)
- [2.2.3 macOS 启动链：Secure ROM / iBoot -> XNU -> launchd（PID 1）](2.2.3_macos_启动链_xnu_与_launchd_初始化/index.md)
- [2.2.4 Windows 启动链：Bootmgr / winload -> ntoskrnl -> smss / csrss / wininit / services.exe](2.2.4_windows_启动链_ntoskrnl_与会话初始化/index.md)

## 导航

← 上一节：[2.1 内核架构、陷入开销与系统调用路径](../2.1_内核架构_陷入开销与系统调用路径/index.md)
↑ 返回上级：[2 内核架构、启动链路、进程与 Daemon/Service 托管](../index.md)
下一节：[2.3 进程、线程生命周期与 Daemon / Service 托管](../2.3_进程_线程生命周期与_daemon_service_托管/index.md) →
