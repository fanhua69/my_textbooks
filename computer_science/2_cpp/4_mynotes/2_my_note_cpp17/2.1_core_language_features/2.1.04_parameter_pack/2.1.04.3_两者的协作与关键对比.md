# 2.1.04.3 两者的协作与关键对比

**介绍**: > **简介**：| 维度 | 模板参数包 | 函数参数包 | | :--- | :--- | :--- | | 所在位置 | `template <...>` 模板参数列表 | `(...)` 函数参数列表 | | 代表内容 | 零个或多个模板参数（类型 / NTTP / 模板模板参数） | 零个或多个函数形参（运行时值/引用）...

---

| 维度 | 模板参数包 | 函数参数包 |
| :--- | :--- | :--- |
| **所在位置** | `template <...>` 模板参数列表 | `(...)` 函数参数列表 |
| **代表内容** | 零个或多个**模板参数**（类型 / NTTP / 模板模板参数） | 零个或多个**函数形参**（运行时值/引用） |
| **常见写法** | `typename... Ts`、`int... Ns` | `Ts... ts`、`Ts&&... ts`、`const Ts&... ts` |
| **包大小查询** | `sizeof...(Ts)` | `sizeof...(ts)`（结果相同，但语义上查的是类型包还是函数参数包） |
| **典型用途** | 类型变换、tuple/索引序列、类模板参数化 | 可变参函数、工厂函数完美转发、批量操作实参 |

## 典型协作示例：同时使用两者的工厂函数
```cpp
#include <memory>
#include <utility>

template <typename T, typename... Args>
std::unique_ptr<T> make_obj(Args&&... args) {
    // T 和 Args... 是模板参数包/参数；args... 是函数参数包
    // std::forward<Args>(args)... 将两个包按索引一一配对展开
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}
```
这里 `Args...` 在模板层定义了**形参类型集合**，在函数参数层定义了**接收实参的形参列表**，最后在 `new T(...)` 处通过 `...` 将它们解包并对齐传递。

---


---

## 导航

- **上一层**：[2.1.04 C++ 参数包（Parameter Pack）详解](../index.md)
- **前一节**：[2.1.04.2 函数参数包（Function Parameter Pack）](../2.1.04.2_%E5%87%BD%E6%95%B0%E5%8F%82%E6%95%B0%E5%8C%85%EF%BC%88Function%20Parameter%20Pack%EF%BC%89/index.md)
- **后一节**：[2.1.04.4 参数包展开（Pack Expansion）的常见方式](../2.1.04.4_%E5%8F%82%E6%95%B0%E5%8C%85%E5%B1%95%E5%BC%80%EF%BC%88Pack%20Expansion%EF%BC%89%E7%9A%84%E5%B8%B8%E8%A7%81%E6%96%B9%E5%BC%8F/index.md)
