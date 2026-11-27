# 2.2.3 macOS 启动链：Secure ROM / iBoot -> XNU -> launchd（PID 1）

**介绍**: 剖析苹果芯片签名验证链、APFS 根卷/快照挂载与 launchd 作为 PID 1 的服务初始化。

## 目录

- [2.2.3.1 Boot ROM、iBoot 阶段与密封 APFS 根卷/系统快照](2.2.3.1_boot_rom_iboot_阶段与密封_apfs_根卷_系统快照/index.md)
- [2.2.3.2 XNU 内核启动与 launchd 域初始化](2.2.3.2_xnu_内核启动与_launchd_域初始化/index.md)

## 导航

← 上一节：[2.2.2 Linux 启动链：固件 -> Bootloader -> initramfs -> systemd（PID 1）](../2.2.2_linux_启动链_initramfs_与_systemd_初始化/index.md)
↑ 返回上级：[2.2 系统启动流程（Boot）与早期初始化](../index.md)
下一节：[2.2.4 Windows 启动链：Bootmgr / winload -> ntoskrnl -> smss / csrss / wininit / services.exe](../2.2.4_windows_启动链_ntoskrnl_与会话初始化/index.md) →
