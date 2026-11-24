# 2.1 右值引用、移动语义与完美转发

掌握值类别基础、T&& 右值引用、移动构造/移动赋值、引用折叠与 std::move / std::forward / std::move_if_noexcept。

## 本节目录

- [2.1.1 左值与右值引用（T&&）及右值对象初始化规则](01_右值引用_t_与右值对象初始化/index.md)
- [2.1.2 移动构造函数、移动赋值运算符与已移后状态（Moved-From State）](02_移动构造_移动赋值与已移后状态/index.md)
- [2.1.3 std::move、std::move if noexcept 与 noexcept 对移动优化的影响](03_std_move_std_move_if_noexcept_与_noexcept/index.md)
- [2.1.4 转发引用（Forwarding Reference）、引用折叠与 std::forward 完美转发](04_转发引用_引用折叠与_std_forward/index.md)

---

## 导航

← 上一节：[1 C++11 演进背景、核心语法与类型推导](../../01_cpp11_overview_syntax_and_type_deduction/index.md)
↑ 返回上级：[2 移动语义、右值引用、Lambda 与编译期计算](../index.md)
下一节：[2.2 Lambda 表达式与闭包对象](../02_lambda_表达式与闭包对象/index.md) →
