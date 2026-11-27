# 2.3 Lambda 增强、强制复制消除与内存/对象生命周期改进

**介绍**: 掌握按值捕获 *this、标准保证的复制消除（Guaranteed Copy Elision）、new T[n]{} 值初始化与对齐感知动态内存分配。

## 目录

- [2.3.1 Lambda 按值捕获 *this（[*this]）与 constexpr Lambda](2.3.1_lambda_捕获_this_与_constexpr_lambda/index.md)
- [2.3.2 强制复制消除（Guaranteed Copy Elision）与 prvalue 纯右值语义重塑](2.3.2_强制复制消除与_prvalue_语义/index.md)
- [2.3.3 new T[n]{} 默认值初始化、过对齐动态内存分配（std::align_val_t）与 std::hardware  destructive interference size](2.3.3_new_值初始化_对齐分配与缓存行常量/index.md)

## 导航

← 上一节：[2.2 折叠表达式（Fold Expressions）、CTAD 与模板参数增强](../2.2_折叠表达式_ctad_与模板参数增强/index.md)
↑ 返回上级：[2 编译期计算、模板增强、Lambda 扩展与对象/内存模型改进](../index.md)
下一节：[3 C++17 现代词汇类型、字符串视图、工具库与容器/算法增强](../../3_cpp17_vocabulary_types_string_view_and_stl_enhancements/index.md) →
