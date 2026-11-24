# 1.1.2.2 标准库实现合并T 和control block分配

介绍：标准库实现合并T 和control block分配

---# `std::make_shared` 与 `std::allocate_shared` 合并内存分配解析

在 C++ 中使用 `std::make_shared<T>(args...)` 或 `std::allocate_shared<T>(alloc, args...)` 创建 `std::shared_ptr<T>` 时，相比传统的 `std::shared_ptr<T>(new T(args...))`，它们会将**控制块（Control Block）**与**目标对象 `T` 的存储空间**合并为**单次内存分配**。

---

## 一、 核心优势是什么？

### 1. 减少一次内存分配开销
创建 `std::shared_ptr<T>(new T(args...))` 通常涉及两次堆内存分配：
1. `new T(args...)` 申请内存并构造对象 `T`；
2. `std::shared_ptr` 构造函数再次申请内存创建控制块。

`make_shared` / `allocate_shared` 将两块内存合并为一次申请：
* 降低堆分配器（`malloc` / `operator new` / 自定义分配器）的调用次数与锁竞争/缓存管理开销；
* 减少内存碎片风险；
* 在单步内完成分配与构造，避免复杂表达式求值顺序带来的潜在资源泄漏隐患。

### 2. 缓存局部性（Cache Locality）更好
CPU 按 **Cache Line（通常为 64 字节）** 从内存加载数据到各级缓存：
* 控制块与 `T` 对象位于同一块连续内存中，访问引用计数与访问 `T` 的成员变量时更容易落在相邻或同一条 Cache Line 中；
* 相比分散在堆上两个位置的内存，**Cache Miss（缓存未命中）** 概率更低，访存效率更高。

### 3. `make_shared` 与 `allocate_shared` 的区别
* `std::make_shared<T>(args...)`：使用默认全局内存分配机制（底层通常走 `::operator new`）。
* `std::allocate_shared<T>(alloc, args...)`：使用传入的自定义分配器 `alloc`（如内存池、对齐分配器、追踪分配器）完成合并分配与后续回收。

---

## 二、 底层是如何实现的？

标准库（如 `libstdc++`、`libc++`）通常通过**“计算合并大小与对齐 + 单次原始分配 + placement new 原地构造 + 析构与释放分离”**实现：

1. **计算总大小与对齐**：定义一个包含控制块元数据（强引用计数 `use_count`、弱引用计数 `weak_count`、自定义删除器/分配器等）以及 `T` 对齐存储区的合并结构体，确保 `T` 的起始地址满足 `alignof(T)`。
2. **发起单次内存分配**：调用分配器的 `allocate` 或 `::operator new` 一次性申请整块原始字节内存。
3. **Placement `new` 原地构造**：
   * 在合并块起始位置构造控制块；
   * 在对齐预留的存储区上通过 placement `new` 并将 `args...` 完美转发（`std::forward<Args>(args)...`）给 `T` 的构造函数。
4. **对象析构与整块内存释放分离**：
   * **强引用计数归零（最后一个 `shared_ptr` 析构）**：立即显式调用 `T` 的析构函数释放 `T` 持有的资源，但**不立即释放整块内存**（因为可能仍有 `weak_ptr` 需要读取控制块状态或尝试 `.lock()`）。
   * **弱引用计数归零（最后一个 `weak_ptr` 也析构）**：销毁控制块，并调用分配器/ `::operator delete` **一次性归还整块内存**。

---

## 三、 简化机制示意代码

以下代码仅用于演示“单次分配 + 原地构造 + 析构与释放分离”的核心机制（实际标准库还包含更完备的对齐计算、分配器传播与异常安全处理）：

```cpp
#include <atomic>
#include <cstddef>
#include <new>
#include <utility>

template <typename T>
struct CombinedBlock {
    std::atomic<long> strong_cnt{1};
    // 1 代表“只要 strong_cnt > 0，该合并块就仍需存活”
    std::atomic<long> weak_cnt{1};

    alignas(T) std::byte storage[sizeof(T)];

    T* obj_ptr() noexcept {
        return reinterpret_cast<T*>(storage);
    }

    template <typename... Args>
    explicit CombinedBlock(Args&&... args) {
        ::new (static_cast<void*>(storage)) T(std::forward<Args>(args)...);
    }

    void release_strong() noexcept {
        if (strong_cnt.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            obj_ptr()->~T();
            release_weak();
        }
    }

    void release_weak() noexcept {
        if (weak_cnt.fetch_sub(1, std::memory_order_acq_rel) == 1) {
            ::operator delete(this);
        }
    }
};

template <typename T, typename... Args>
CombinedBlock<T>* make_combined(Args&&... args) {
    void* raw = ::operator new(sizeof(CombinedBlock<T>));
    return ::new (raw) CombinedBlock<T>(std::forward<Args>(args)...);
}
```

---

## 四、 工程注意点

* **内存释放延迟**：由于控制块与 `T` 共享同一块内存，即使 `T` 已经析构，只要还有存活的 `std::weak_ptr`，整块内存就不会归还给分配器。若 `T` 占用内存很大且 `weak_ptr` 生命周期很长，需评估这一代价（必要时改用 `std::shared_ptr<T>(new T(...))`）。
```
## 导航

- **上一层**：[父级](../index.md)
- **前一节**：[TODO_PREV]
- **后一节**：[TODO_NEXT]
