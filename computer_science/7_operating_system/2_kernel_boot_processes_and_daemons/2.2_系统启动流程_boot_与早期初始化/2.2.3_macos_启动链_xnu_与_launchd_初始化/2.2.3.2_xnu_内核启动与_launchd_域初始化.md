# 2.2.3.2 XNU 内核启动与 launchd 域初始化

**介绍**: 梳理 BSD/Mach 初始化完成后拉起 launchd（PID 1）及系统域、用户会话域建立的流程。

---

## 导航

← 上一节：[2.2.3.1 Boot ROM、iBoot 阶段与密封 APFS 根卷/系统快照](../2.2.3.1_boot_rom_iboot_阶段与密封_apfs_根卷_系统快照/index.md)
↑ 返回上级：[2.2.3 macOS 启动链：Secure ROM / iBoot -> XNU -> launchd（PID 1）](../index.md)
下一节：[2.2.4 Windows 启动链：Bootmgr / winload -> ntoskrnl -> smss / csrss / wininit / services.exe](../../2.2.4_windows_启动链_ntoskrnl_与会话初始化/index.md) →
