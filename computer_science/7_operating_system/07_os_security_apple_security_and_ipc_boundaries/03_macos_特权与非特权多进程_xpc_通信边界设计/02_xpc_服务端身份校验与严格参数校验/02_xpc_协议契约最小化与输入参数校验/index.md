# 02 XPC 协议契约最小化、NSSecureCoding 白名单与参数合法性校验

**介绍**: 缩小特权暴露面、校验路径/整数/枚举/长度边界，防止恶作剧或受损客户端触发越权操作。

---

## 导航

← 上一节：[7.3.2.1 基于 Audit Token 与 SecCode/Signing Requirement 的对端认证](../01_基于_audit_token_与_signing_requirement_的对端认证/index.md)
↑ 返回上级：[7.3.2 XPC 服务端调用方校验（Audit Token / Signing Requirement）与严格参数校验](../index.md)
下一节：[7.3.3 XPC 控制面与高速数据面解耦及崩溃隔离](../../03_xpc_控制面与高速数据面解耦及崩溃隔离/index.md) →
