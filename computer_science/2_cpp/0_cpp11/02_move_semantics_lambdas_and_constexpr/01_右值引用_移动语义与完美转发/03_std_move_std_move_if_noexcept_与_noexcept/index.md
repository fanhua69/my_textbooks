# 2.1.3 std::move、std::move if noexcept 与 noexcept 对移动优化的影响

理解 std::move 的无条件强转本质、noexcept 说明符与 noexcept 运算符，以及 std::vector 重分配时依赖 noexcept 决定移动或拷贝。

---

## 导航

← 上一节：[2.1.2 移动构造函数、移动赋值运算符与已移后状态（Moved-From State）](../02_移动构造_移动赋值与已移后状态/index.md)
↑ 返回上级：[2.1 右值引用、移动语义与完美转发](../index.md)
下一节：[2.1.4 转发引用（Forwarding Reference）、引用折叠与 std::forward 完美转发](../04_转发引用_引用折叠与_std_forward/index.md) →
