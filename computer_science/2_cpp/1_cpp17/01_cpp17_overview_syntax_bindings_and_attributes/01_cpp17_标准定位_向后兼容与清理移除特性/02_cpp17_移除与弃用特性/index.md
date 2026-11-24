# 02 C++17 移除与弃用特性（动态异常规格移除、register/auto ptr 移除、三字符组移除等）

**介绍**: 掌握 throw(T) 动态异常说明移除（仅保留 throw() 作 noexcept(true) 别名）、register 关键字移除、std::auto_ptr 与 std::random_shuffle 移除、三字符组（Trigraphs）移除及 operator++(bool) 移除。

---

## 导航

← 上一节：[1.1.1 从 C++11/14 到 C++17：工程实用性与现代词汇类型落地](../01_从_cpp11_14_到_cpp17_工程实用性与现代词汇类型/index.md)
↑ 返回上级：[1.1 C++17 标准定位、向后兼容与清理/移除特性](../index.md)
下一节：[1.1.3   has include 预处理器条件与嵌套命名空间（namespace A::B::C）](../03_has_include_与嵌套命名空间/index.md) →
