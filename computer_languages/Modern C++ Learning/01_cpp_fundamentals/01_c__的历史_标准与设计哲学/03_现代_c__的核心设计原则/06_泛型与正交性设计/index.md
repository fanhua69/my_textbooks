# 1.1.3.6 泛型与正交性设计（Orthogonality & Generic Programming）

算法与数据结构正交解耦，以严格复杂度为接口契约，静态多态优先于动态多态。

---

## 导航

← 上一节：[1.1.3.5 值语义优先与移动语义流转](../05_值语义优先与移动语义流转/index.md)
↑ 返回上级：[1.1.3 现代 C++ 的核心设计原则](../index.md)
下一节：[1.1.4 如何阅读标准、提案与编译器文档](../../04_如何阅读标准_提案与编译器文档/index.md) →

---

## 1. Stepanov 正交模型

C++ 的标准模板库（STL）由 Alexander Stepanov 精心构建，它奠定了现代 C++ 极其崇尚的**正交性（Orthogonality）**架构哲学：**数据结构（容器）与操作算法在逻辑上应当是完全解耦、互不依赖的**。

```mermaid
flowchart LR
    Containers["数据结构 (Containers)<br/>vector, list, deque..."] 
    <-->|"统一抽象黏合剂: 迭代器 (Iterators)"| 
    Algorithms["算法族 (Algorithms)<br/>sort, find, transform..."]
```

在传统的纯面向对象系统（如某些 Java 体系）中，如果要在容器中实现排序，通常需要为容器类添加 `.sort()` 成员方法，或者让容器内的元素实现统一的 `Comparable` 接口。这就将容器与算法深度耦合在一起：$N$ 个容器如果要支持 $M$ 种算法，需要编写大量的适配代码。

现代 C++ STL 的设计将二者彻底解耦：
- **容器** 只专注负责内存布局与生命周期管理，对外暴露合规的迭代器；
- **算法** 是纯函数式自由函数，仅通过泛型迭代器访问数据，对具体容器的内部实现一无所知；
- 两者通过**迭代器抽象（C++20 升级为 Ranges 与 Views）**无缝协作。只需编写 $N$ 个容器和 $M$ 个算法，就能自动获得 $N \times M$ 种组合能力！

---

## 2. 明确的复杂度保障作为接口契约

在现代 C++ 中，标准委员会对 STL 的每一种容器操作和算法都**在标准规范文本中严格锁定了时间复杂度下限**：
- `std::vector::push_back` 必须保证平摊常数时间复杂度 $\mathcal{O}(1)$；
- `std::map::find` 必须严格为对数时间复杂度 $\mathcal{O}(\log n)$；
- `std::unordered_map::find` 平均为常数复杂度 $\mathcal{O}(1)$；
- `std::sort` 最坏情况下必须达到 $\mathcal{O}(n \log n)$（杜绝了早期朴素快速排序恶化到 $\mathcal{O}(n^2)$ 的安全漏洞）。

> [!IMPORTANT]
> 现代 C++ 强调：**没有复杂度约束的抽象是虚假的抽象**。程序员调用接口时，不仅拥有类型系统赋予的安全性，更拥有底层性能与时延的确定性预期。

---

## 3. C++ Core Guidelines 核心守则摘要

由 Bjarne Stroustrup 与 Herb Sutter 联合制定的 [**C++ Core Guidelines**](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) 是现代 C++ 工业界实践的集大成者。它凝练成了指导我们编写现代 C++ 代码的行动指南：

1. **资源与所有权**：
   - 绝不使用裸指针（`T*`）表示所有权；裸指针仅用作借用（Borrowing）或非拥有式观察（Non-owning Observer）。
   - 绝不显式调用 `delete` 或 `free`；让容器与智能指针管理生命周期。
2. **函数设计**：
   - 优先通过返回值向外传递数据，避免使用非 `const` 引用形参充当出参。
   - 对小对象（小于等于 2~3 个指针大小，如 `int`、`std::string_view`、`std::span`）优先按值传递；对大对象优先按 `const T&` 传递。
3. **常量性与不可变性**：
   - 尽可能将局部变量、成员函数声明为 `const`；不可变性天然杜绝错误并助力编译器极致优化。
   - 只要能在编译期确定的值或逻辑，坚决声明为 `constexpr`。
4. **面向对象与多态**：
   - 如果一个类具备虚函数，其析构函数**必须**声明为 `public virtual` 或 `protected non-virtual`。
   - 重写基类虚函数时，**始终且仅使用** `override` 关键字。
