# 02 Linux 启动链：固件 -> Bootloader -> initramfs -> systemd（PID 1）

**介绍**: 掌握早期用户态钩子、root 切换、Unit 依赖解析、Socket/D-Bus 激活与并行服务拉起。

## 目录

- [01 initramfs 阶段、udev 设备冷插拔与 switch  root](01_initramfs_阶段_udev_设备冷插拔与_switch_root/index.md)
- [02 systemd PID 1 初始化、Target 依赖与并行启动](02_systemd_pid_1_初始化_target_依赖与并行启动/index.md)

## 导航

← 上一节：[2.2.1 固件引导（UEFI / iBoot）、Bootloader 与内核早期初始化](../01_固件引导_uefi_iboot_bootloader_与早期初始化/index.md)
↑ 返回上级：[2.2 系统启动流程（Boot）与早期初始化](../index.md)
下一节：[2.2.3 macOS 启动链：Secure ROM / iBoot -> XNU -> launchd（PID 1）](../03_macos_启动链_xnu_与_launchd_初始化/index.md) →
