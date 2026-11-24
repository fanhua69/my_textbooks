# 02 mach msg() 消息结构与 Out-of-Line（OOL）内存描述符

**介绍**: 剖析内联数据与写时复制（COW）跨进程虚拟内存页传输原理。

---

## 导航

← 上一节：[3.1.1 Mach Port、Send/Receive Rights 与端口命名空间](../01_mach_port_send_receive_rights_与端口命名空间/index.md)
↑ 返回上级：[3.1 XNU 混合内核与 Mach Ports 底层原语](../index.md)
下一节：[3.1.3 Bootstrap Server 与 launchd 服务注册机制](../03_bootstrap_server_与_launchd_服务注册机制/index.md) →
