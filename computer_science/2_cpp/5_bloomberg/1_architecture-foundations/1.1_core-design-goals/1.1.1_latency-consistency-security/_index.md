# 1.1.1 Latency, Consistency & Security Trade-offs

**介绍**: 探讨金融权限（Entitlement）系统在亚微秒/微秒级低延迟查询、数据一致性与安全合规之间的核心工程权衡，重点分析高并发热路径尾延迟（P99 / P99.9）与权限变更/撤销实时性之间的矛盾与折中方案。


## 目录

- [1.1.1.1 核心工程矛盾：不可能三角的三方拉锯](1.1.1.1_核心工程矛盾：不可能三角的三方拉锯.md)
- [1.1.1.2 Fail_Closed 安全降级是啥意思](1.1.1.2_Fail_Closed.md)
- [1.1.1.3 维度拆解与权衡矩阵](1.1.1.3_维度拆解与权衡矩阵.md)
- [1.1.1.4 C++17 热路径查询示意](1.1.1.4_C%2B%2B17%20%E7%83%AD%E8%B7%AF%E5%BE%84%E6%9F%A5%E8%AF%A2%E7%A4%BA%E6%84%8F.md)
- [1.1.1.5 面试与架构评审要点](1.1.1.5_面试与架构评审要点.md)

---

## 导航

⬅️ 上一节：无（这是本目录的第一页）
⏺️ 当前节：[1.1.1 Latency, Consistency & Security Trade-offs](_index.md)
➡️ 下一节：[1.1.2 Public API vs. Backend Optimizations（对外接口稳定性与后端深度优化的博弈）](../1.1.2_public-api-vs-backend-optimizations.md)
⬆️ 返回上级：[1.1 core design goals](../_index.md)
