# 1.1.3.5 值语义优先与移动语义流转（Value Semantics & Move Semantics）

拥抱默认独立深拷贝与无别名安全，通过右值引用与移动语义消除拷贝代价。

---

## 导航

← 上一节：[1.1.3.4 计算前置与编译期求值](../04_计算前置与编译期求值/index.md)
↑ 返回上级：[1.1.3 现代 C++ 的核心设计原则](../index.md)
下一节：[1.1.3.6 泛型与正交性设计](../06_泛型与正交性设计/index.md) →

---

## 1. 为什么现代软件工程偏爱“值语义”？

现代软件工程极其痛恨**隐式共享可变状态（Shared Mutable State）**，因为它是并发数据竞争、内存双重释放与内存破坏的第一大元凶。

在值语义下，每个变量都拥有其独立的存储空间。对一个变量的修改绝不会在暗地里影响其他变量（无意外的别名副作用，No Spooky Action at a Distance）：

```cpp
#include <string>

void demo_value_semantics() {
    std::string a = "Hello";
    std::string b = a; // 深度拷贝：独立内存空间
    b += " World";     // 修改 b 绝不会波及 a 的内容！
}
```

然而在 C++98 时代，严格坚持值语义需要付出昂贵的代价：当一个对象内部持有着数兆字节的动态数组时，拷贝操作意味着大规模的堆内存分配与数据搬移。这迫使大量 C++98 程序员退回到底层指针传递或引用出参（Out Parameters）。

---

## 2. 移动语义：对值语义的现代救赎

C++11 引入的**右值引用（`T&&`）与移动语义（Move Semantics）**，一举解决了“值语义的美好设计”与“深拷贝的性能开销”之间的根本矛盾：

```mermaid
flowchart TD
    subgraph Copy ["古典深拷贝 (Deep Copy): 昂贵的内存分配与全量复制"]
        A1["源对象 (资源所有者)"] -->|深拷贝| A2["新分配堆内存<br/>(复制数十万元素)"]
    end

    subgraph Move ["现代移动语义 (Move Semantics): 极速的所有权浅层窃取"]
        B1["临时源对象 (即将消亡)"] -->|"交换指针与长度 (8~24 字节)"| B2["目标对象"]
        B2 -->|"接管原有堆内存"| Heap["已有堆数据 (无需拷贝)"]
        B1 -.->|"设为空指针 (安全析构)"| Null["nullptr"]
    end
```

---

## 3. 现代传参与返回值标准范式

得益于移动语义与编译器的**具名返回值优化（NRVO / RVO）**，现代 C++ 的编程风格发生了极具表达力的跃迁：

```cpp
#include <vector>
#include <string>
#include <utility>

// 现代规范 1：重量级对象应当直接“按值返回”！
// 绝不再像 C++98 那样传递 (std::vector<int>& out_result)
std::vector<std::string> create_large_dataset() {
    std::vector<std::string> data;
    data.reserve(100000);
    // 填充数据...
    return data; // RVO 保证零拷贝；即使无法优化，也会触发移动构造，仅仅是指针交换！
}

// 现代规范 2：需要保留副本的场景，推荐“按值传参并 std::move”
class Employee {
    std::string name_;
    std::vector<int> scores_;
public:
    // 一个构造函数兼顾“左值传入时拷贝”与“右值传入时移动”，达到最佳灵活性与效率
    Employee(std::string name, std::vector<int> scores)
        : name_(std::move(name)), scores_(std::move(scores)) {}
};
```
