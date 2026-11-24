# 2.2.2.1 initramfs 阶段、udev 设备冷插拔与 switch  root

梳理初始内存盘加载存储/文件系统驱动、创建设备节点与切换至真实根文件系统的过程。

---

## 导航

← 上一节：[2.2.1 固件引导（UEFI / iBoot）、Bootloader 与内核早期初始化](../../01_固件引导_uefi_iboot_bootloader_与早期初始化/index.md)
↑ 返回上级：[2.2.2 Linux 启动链：固件 -> Bootloader -> initramfs -> systemd（PID 1）](../index.md)
下一节：[2.2.2.2 systemd PID 1 初始化、Target 依赖与并行启动](../02_systemd_pid_1_初始化_target_依赖与并行启动/index.md) →
