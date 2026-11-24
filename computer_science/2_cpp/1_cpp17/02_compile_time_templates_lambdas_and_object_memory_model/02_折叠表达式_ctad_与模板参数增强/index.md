# 2.2 折叠表达式（Fold Expressions）、CTAD 与模板参数增强

掌握一元/二元折叠表达式简化变参包运算、类模板实参推导（CTAD）与推导指引、auto 非类型模板参数及包展开 using 声明。

## 本节目录

- [2.2.1 一元左右折叠与二元左右折叠表达式（(... op pack) / (pack op ...) / (init op ... op pack)）](01_一元与二元折叠表达式/index.md)
- [2.2.2 类模板实参推导（CTAD）、推导指引（Deduction Guides）与 auto 列表初始化推导](02_ctad_推导指引与_auto_花括号推导/index.md)
- [2.2.3 auto 非类型模板参数（template <auto N>）、包展开 using 声明与模板模板参数匹配放宽](03_auto_非类型模板参数与模板规则放宽/index.md)

---

## 导航

← 上一节：[2.1 if constexpr 编译期分支与 constexpr 扩展](../01_if_constexpr_与_constexpr_扩展/index.md)
↑ 返回上级：[2 编译期计算、模板增强、Lambda 扩展与对象/内存模型改进](../index.md)
下一节：[2.3 Lambda 增强、强制复制消除与内存/对象生命周期改进](../03_lambda_增强_强制复制消除与内存分配改进/index.md) →
