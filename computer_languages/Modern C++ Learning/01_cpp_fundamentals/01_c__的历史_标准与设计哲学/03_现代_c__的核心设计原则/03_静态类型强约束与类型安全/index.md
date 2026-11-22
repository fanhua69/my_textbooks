# 1.1.3.3 静态类型强约束与类型安全（Static Type Safety）

把运行期隐患尽可能扼杀在编译期。掌握强类型枚举、强类型物理单位与 C++20 Concepts 显式契约。

---

## 导航

← 上一节：[1.1.3.2 RAII 与确定性生命周期](../02_raii_与确定性生命周期/index.md)
↑ 返回上级：[1.1.3 现代 C++ 的核心设计原则](../index.md)
下一节：[1.1.3.4 计算前置与编译期求值](../04_计算前置与编译期求值/index.md) →

---

## 1. 静态检查哲学

现代 C++ 极为推崇**静态检查（Static Checking）**。其哲学可总结为：**任何能够在编译期发现的逻辑漏洞，决不能推迟到运行期；任何能够通过类型系统表达的约束，绝不退化为裸类型或弱类型**。

---

## 2. 强类型枚举与类型安全

古典 C++ 的 `enum` 会自动污染外层命名空间，并且会隐式衰减为整型数值，极易造成意料之外的越界赋值与逻辑混乱。

```cpp
// 古典 C++98: 非强类型枚举（枚举量暴露在外层作用域）
enum Color { Color_Red, Color_Green, Color_Blue };
// enum AlertLevel { Green, Yellow, Red }; // 若写成与上方同名，直接编译报错：Red/Green 已被占用！

// 现代 C++: 强类型作用域枚举
enum class TrafficLight : uint8_t { Red, Yellow, Green };
enum class LogSeverity  : uint8_t { Debug, Info, Warning, Error };

void demo_enum_safety() {
    TrafficLight light = TrafficLight::Red;
    // if (light == 0) {}                  // 编译错误：禁止整型与枚举隐式混用！
    // if (light == LogSeverity::Error) {} // 编译错误：不同枚举强类型绝不相混！
}
```

---

## 3. 强类型单位防范灾难事故

在系统编程中，不同物理单位之间的混淆曾多次酿成航天级灾难（如火星气候探测者号因英制与公制单位未区分而坠毁）。现代 C++ 标准库中的 `std::chrono` 堪称强类型系统的教科书级实践：

```cpp
#include <chrono>
#include <thread>

using namespace std::chrono_literals;

// 错误示范：裸整型传参，调用方完全不知道入参是秒、毫秒还是微秒
void sleep_legacy(int duration_val); 

// 正确示范：强类型持续时间约束
void sleep_modern(std::chrono::milliseconds dur) {
    std::this_thread::sleep_for(dur);
}

void test_chrono() {
    sleep_modern(500ms);  // 合法：精确为 500 毫秒
    sleep_modern(2s);     // 合法：自动将 2 秒无损提升转换为 2000 毫秒
    // sleep_modern(1500us); // 编译错误！微秒转换到毫秒存在精度丢失，编译器拒绝隐式转换！
    // 必须显式指明截断方式：
    sleep_modern(std::chrono::duration_cast<std::chrono::milliseconds>(1500us));
}
```

---

## 4. C++20 Concepts（概念）：告别隐式鸭子类型

在 C++20 之前，模板属于隐式的鸭子类型——只要代码在展开时能够编译通过即可。一旦调用方传入了缺少某些方法或操作符的类型，编译器会报出深达几十层的模板内部实例化调用栈，极其晦涩。

C++20 引入的 **Concepts（概念）** 将静态类型约束提升为第一类公民：

```cpp
#include <concepts>
#include <iostream>

// 定义可打印且支持大小比较的语义概念
template <typename T>
concept PrintableOrdered = std::totally_ordered<T> && requires(T a, std::ostream& os) {
    { os << a } -> std::same_as<std::ostream&>;
};

// 带有强约束概念的泛型函数
template <PrintableOrdered T>
void print_maximum(const T& a, const T& b) {
    std::cout << "Max: " << (a > b ? a : b) << '\n';
}

struct Point {
    int x, y;
    // 缺少 operator> 与 operator<<
};

void test_concept() {
    print_maximum(10, 20); // 编译通过：int 满足完全偏序与输出流约束
    
    Point p1{1, 2}, p2{3, 4};
    // print_maximum(p1, p2); 
    // 现代编译器精准报错：'Point' does not satisfy constraint 'PrintableOrdered'
    // 不再报出一行模板内部展开的杂音，直接定位根因！
}
```
