# 2.1.04 C++ 参数包（Parameter Pack）详解

**介绍**: **参数包（Parameter Pack）** 是 C++11 引入的核心特性，主要用于**可变参数模板（Variadic Templates）**，允许模板接受**零个或多个**任意类型的模板参数或函数参数。它是实现 `std::tuple`、`std::make_shared`、`std::printf` 安全替代品等现代 C++ 设施的基础。

核心语法符号是省略号 `...`：
* **声明时**：`...` 在参数名**左侧**（打包）。
* **展开时**：`...` 在表达式**右侧**（解包）。

---

## 小节索引

- [2.1.04.1 模板参数包（Template Parameter Pack）](./2.1.04.1_模板参数包（Template%20Parameter%20Pack）/index.md)
- [2.1.04.2 函数参数包（Function Parameter Pack）](./2.1.04.2_函数参数包（Function%20Parameter%20Pack）/index.md)
- [2.1.04.3 两者的协作与关键对比](./2.1.04.3_两者的协作与关键对比/index.md)
- [2.1.04.4 参数包展开（Pack Expansion）的常见方式](./2.1.04.4_参数包展开（Pack%20Expansion）的常见方式/index.md)
- [2.1.04.5 展开模式（Pattern）速查表](./2.1.04.5_展开模式（Pattern）速查表/index.md)


---

## 导航

- **后一节**：[2.1.04.1 模板参数包（Template Parameter Pack）](2.1.04.1_%E6%A8%A1%E6%9D%BF%E5%8F%82%E6%95%B0%E5%8C%85%EF%BC%88Template%20Parameter%20Pack%EF%BC%89/index.md)
