# 7.3.2 XPC 服务端调用方校验（Audit Token / Signing Requirement）与严格参数校验

利用内核签发的 Audit Token 结合代码签名校验连接合法性，实施协议白名单、安全编解码与输入边界检查。

## 本节目录

- [7.3.2.1 基于 Audit Token 与 SecCode/Signing Requirement 的对端认证](01_基于_audit_token_与_signing_requirement_的对端认证/index.md)
- [7.3.2.2 XPC 协议契约最小化、NSSecureCoding 白名单与参数合法性校验](02_xpc_协议契约最小化与输入参数校验/index.md)

---

## 导航

← 上一节：[7.3.1 特权分离架构：非特权客户端与特权服务端划分](../01_特权分离架构_客户端与特权服务端划分/index.md)
↑ 返回上级：[7.3 macOS 特权与非特权多进程 XPC 通信边界设计](../index.md)
下一节：[7.3.3 XPC 控制面与高速数据面解耦及崩溃隔离](../03_xpc_控制面与高速数据面解耦及崩溃隔离/index.md) →
