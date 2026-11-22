# 9.3.2.1 CI 流水线阶段设计与 DAG 并发加速

设计 代码拉取 -> Lint 校验 -> 单元测试 -> 构建制品 -> 集成测试 的阶段流水线，通过 DAG 拓扑实现任务最大并发。

---

## 导航

← 上一节：[9.3.1 DevOps 文化与 CALMS 价值模型](../../01_devops_culture_and_calms/index.md)
↑ 返回上级：[9.3.2 持续集成 (CI) 流水线工程](../index.md)
下一节：[9.3.2.2 制品库管理与不可变构建制品](../02_immutable_artifact_repository/index.md) →
