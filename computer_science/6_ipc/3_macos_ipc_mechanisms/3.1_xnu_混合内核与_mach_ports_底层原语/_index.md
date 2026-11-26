# 3.1 XNU 混合内核与 Mach Ports 底层原语

**介绍**: 探究苹果操作系统 IPC 的微内核基石：Mach 消息传递与端口权限模型。


## 目录

- [3.1.1 Mach Port、Send/Receive Rights 与端口命名空间](3.1.1_mach_port_send_receive_rights_与端口命名空间/_index.md)
- [3.1.2 mach msg() 消息结构与 Out-of-Line（OOL）内存描述符](3.1.2_mach_msg_消息结构与_out_of_line_ool_内存描述符/_index.md)
- [3.1.3 Bootstrap Server 与 launchd 服务注册机制](3.1.3_bootstrap_server_与_launchd_服务注册机制/_index.md)

---

## 导航

⬅️ 上一节：无（这是本目录的第一页）
⏺️ 当前节：[3.1 XNU 混合内核与 Mach Ports 底层原语](_index.md)
➡️ 下一节：[3.2 XPC 框架：macOS 现代 IPC 核心](../3.2_xpc_框架_macos_现代_ipc_核心/_index.md)
⬆️ 返回上级：[3 macOS（XNU / Darwin）平台 IPC 机制深度剖析](../_index.md)
