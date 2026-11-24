# 1.1.09.1 unique_pointer

**介绍**: fsdafsad

---

## 1. 核心特性与零开销原则

* **独占所有权**：不可拷贝构造（`unique_ptr(const unique_ptr&) = delete`），也不可拷贝赋值（`operator=(const unique_ptr&) = delete`），从而杜绝双释放（double free）和所有权模糊。
* **支持移动语义**：可通过 `std::move` 或函数返回值转移所有权；转移后源指针置为 `nullptr`。
* **接近裸指针的开销**：默认删除器 `std::default_delete<T>` 在无状态时通常为空类优化（EBO），大小与裸指针相当，解引用与裸指针几乎一致。
* **支持数组特化**：提供 `std::unique_ptr<T[]>`，析构时自动调用 `delete[]` 而不是 `delete`。

---

## 2. 创建、转移与常用接口

```cpp
#include <iostream>
#include <memory>
#include <utility>

struct Resource {
    int id;
    explicit Resource(int x) : id(x) {
        std::cout << "Resource(" << id << ") acquired\n";
    }
    ~Resource() {
        std::cout << "Resource(" << id << ") released\n";
    }
};

std::unique_ptr<Resource> make_resource(int id) {
    auto ptr = std::make_unique<Resource>(id); // C++14 推荐
    return ptr; // 满足移动/NRVO，可直接返回
}

void take_ownership(std::unique_ptr<Resource> ptr) {
    if (ptr) {
        std::cout << "Now owning Resource(" << ptr->id << ")\n";
    }
} // 函数结束时自动析构释放

int main() {
    auto p1 = make_resource(1);

    // 1. 转移所有权
    auto p2 = std::move(p1);
    std::cout << "p1 is " << (p1 ? "valid" : "null") << '\n'; // null
    take_ownership(std::move(p2));
    std::cout << "p2 is " << (p2 ? "valid" : "null") << '\n'; // null

    // 2. 观察裸指针（不转移所有权）
    auto p3 = std::make_unique<Resource>(3);
    Resource* raw = p3.get();
    std::cout << "raw id = " << raw->id << '\n';

    // 3. reset() 与 release()
    p3.reset(new Resource(4)); // 先销毁 Resource(3)，再托管 Resource(4)
    Resource* detached = p3.release(); // 放弃所有权并返回裸指针，需手动管理
    delete detached;

    // 4. 数组形式 std::unique_ptr<T[]>
    auto arr = std::make_unique<int[]>(5);
    for (int i = 0; i < 5; ++i) {
        arr[i] = i * 10;
    }
    std::cout << "arr[2] = " << arr[2] << '\n';
}
```

---

## 3. 自定义删除器（Deleter）

当管理文件句柄、C 接口资源、Socket 或特定释放函数时，可以传入自定义删除器：

```cpp
#include <cstdio>
#include <iostream>
#include <memory>

struct FileCloser {
    void operator()(std::FILE* fp) const noexcept {
        if (fp) {
            std::fclose(fp);
            std::cout << "FILE* closed\n";
        }
    }
};

int main() {
    // 1. 函数对象删除器（推荐，便于空基类优化）
    std::unique_ptr<std::FILE, FileCloser> fp(
        std::fopen("demo_unique_ptr.txt", "w")
    );
    if (fp) {
        std::fputs("hello unique_ptr\n", fp.get());
    }

    // 2. Lambda 删除器（注意模板参数需传入 decltype(deleter)）
    auto custom_deleter = [](int* p) {
        std::cout << "custom delete value = " << (p ? *p : 0) << '\n';
        delete p;
    };
    std::unique_ptr<int, decltype(custom_deleter)> num(
        new int(99), custom_deleter
    );
}
```

---

## 4. 常见坑点与最佳实践

1. **优先使用 `std::make_unique`（C++14）**：避免手写 `new`，在复杂表达式中也能防止因求值顺序或异常导致的内存泄漏。
2. **不要用同一裸指针构造多个智能指针**：`Resource* r = new Resource(1); std::unique_ptr<Resource> a(r); std::unique_ptr<Resource> b(r);` 会导致两次 `delete`（未定义行为）。
3. **函数传参优先传 `T&` 或 `const T&`**：如果函数只是使用对象而不接管生命周期，传 `Resource&` 或 `const Resource&` 比传 `unique_ptr` 更通用；只有明确要接管所有权时才按值传 `std::unique_ptr<Resource>`。
4. **需要共享所有权时再升级为 `std::shared_ptr`**：`std::unique_ptr<T>` 可以直接隐式转换为 `std::shared_ptr<T>`（通过移动语义），设计上应默认 `unique_ptr`，仅在确实需要共享生命周期时引入 `shared_ptr`。

---

## 导航

- **上一层**：[父级](../index.md)
- **前一节**：[1.1.08 lambda function](../../1.1.08_lambda_function/index.md)
- **后一节**：[1.1.09.2 shared pointer](../1.1.09.2_shared_pointer/index.md)


---

## 导航

- **上一层**：[父级](../index.md)
- **前一节**：[1.1.08 lambda function](../../1.1.08_lambda_function/index.md)
- **后一节**：[1.1.09.2 shared pointer](../1.1.09.2_shared_pointer/index.md)
