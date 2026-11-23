# 1.3.1.2 Non-blocking 算法与“线程暂停”的本质区别

> **简介**：Non-blocking Algorithm（非阻塞算法）的核心思想是：一个线程的暂停或延迟，不应该阻止其他线程继续完成它们的操作。系统不依赖某个特定线程必须恢复运行或释放锁，其余活跃线程依然能够通过自身推进或协作完成状态迁移。

---

## 什么是 Non-blocking 算法？

**Non-blocking Algorithm（非阻塞算法）**的核心思想是：**一个线程的暂停或延迟，不应该阻止其他线程继续完成它们的操作**。系统不依赖某个特定线程必须恢复运行或释放锁，其余活跃线程依然能够通过自身推进或协作完成状态迁移。

在现代多核硬件上，非阻塞算法通常依托原子操作（Atomic Operations）构建，例如：
- **Compare-And-Swap（CAS）**（`compare_exchange_weak` / `compare_exchange_strong`）
- **Fetch-And-Add（FAA）**（`fetch_add`）
- **Load-Link / Store-Conditional（LL/SC）** 等底层原子原语

### 1. 为什么 CAS、FAA 与 LL/SC 能做到非阻塞（Non-blocking）？

在并发系统中，**Non-blocking（非阻塞）**的核心并不是“线程永不暂停”或“代码里没有 `std::mutex`”，而是**一个线程的暂停或延迟，不会阻止其他线程继续完成操作**。

传统基于锁的同步存在“持锁 -> 暂停 -> 其他线程卡住等待”的**进度依赖（Progress Dependency）**；而 **CAS**、**FAA** 与 **LL/SC** 之所以能支撑非阻塞算法，是因为它们把“读-改-写”收敛到了**硬件保证不可分割的原子状态跃迁**中，没有跨指令周期的独占锁持有期。

---

### 2. Compare-And-Swap（CAS：`compare_exchange_weak` / `compare_exchange_strong`）

CAS 的语义是：**“若目标内存当前值等于我看到的 `expected`，就原子地将其更新为 `desired` 并返回 `true`；否则不修改内存，把当前实际值写回 `expected` 并返回 `false`。”**

### 如何避免因单线程暂停而阻塞他人？

- **无独占持有期**：线程 `A` 读取当前状态 `expected` 后即使被操作系统暂停，它也没有持有任何锁或独占标记。
- **冲突即重试、互不卡死**：若 `A` 暂停期间，线程 `B` 抢先完成 CAS 推进了状态，`A` 恢复后尝试 CAS 会失败，但会立刻拿到最新值并在本地重新计算后重试；`A` 不会阻塞 `B`，`B` 也不需要等 `A`。

### 无锁 C++ 示例（CAS 推进栈顶指针）

```cpp
#include <atomic>

struct Node {
    int value;
    Node* next;
};

class LockFreeStack {
public:
    void push(int v) {
        Node* node = new Node{v, nullptr};
        node->next = head_.load(std::memory_order_relaxed);
        while (!head_.compare_exchange_weak(
            node->next, node,
            std::memory_order_release,
            std::memory_order_relaxed)) {
            // 若其他线程抢先修改了 head_，node->next 会自动更新为最新值并继续重试
        }
    }

private:
    std::atomic<Node*> head_{nullptr};
};
```


## 警惕两个常见误区

1. **Non-blocking $\neq$ 线程不会被操作系统暂停**
   在现代操作系统的对抗性调度模型下，任何线程都可能在任意两条机器指令之间被抢占或延迟。区别在于：**Blocking** 下 Thread A 被暂停可能导致 Thread B 无法完成操作；**Non-blocking** 下 Thread A 被暂停，Thread B（以及 Thread C）依然能够继续取得进展。
2. **使用了 `std::atomic` / CAS $\neq$ 一定是 Non-blocking 或 Lock-Free**
   即便没有 `std::mutex`，如果代码逻辑上强依赖某个特定线程完成某一步之后其他线程才能继续，或者用原子变量搭出了自旋锁（Spinlock），依然属于阻塞依赖；即便只是普通的 CAS 循环，如果某线程反复冲突失败、而其他线程不断成功，也只说明系统整体在推进，不代表单个线程不会遭遇饥饿（Starvation）或自旋等待（Spin Waiting）。

## Blocking 与 Non-blocking 特征对照

| 特征维度 | Blocking 算法 | Non-blocking 算法 |
| :--- | :--- | :--- |
| **是否可能发生线程暂停/调度** | 是 | 是 |
| **是否依赖特定线程恢复才能推进** | 可能依赖 | 不依赖 |
| **是否保证系统整体进度** | 不保证（持锁线程停摆可拖垮等待者） | 取决于具体进度保证等级（Obstruction-Free / Lock-Free / Wait-Free） |
| **典型同步手段** | `std::mutex`、条件变量、信号量或原子自旋锁 | 原子读-改-写指令（CAS、FAA 等）与无锁状态机 |

---


---

## 导航

- **上一层**：[1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms](../index.md)
- **前一节**：[1.3.1.1 根本问题与 Blocking 算法：当线程被暂停时，其他线程还能继续吗？](../1.3.1.1_%E6%A0%B9%E6%9C%AC%E9%97%AE%E9%A2%98%E4%B8%8E%20Blocking%20%E7%AE%97%E6%B3%95%EF%BC%9A%E5%BD%93%E7%BA%BF%E7%A8%8B%E8%A2%AB%E6%9A%82%E5%81%9C%E6%97%B6%EF%BC%8C%E5%85%B6%E4%BB%96%E7%BA%BF%E7%A8%8B%E8%BF%98%E8%83%BD%E7%BB%A7%E7%BB%AD%E5%90%97%EF%BC%9F/index.md)
- **后一节**：[1.3.1.3 三种 Non-blocking Progress Guarantees（进度保证）概览](../1.3.1.3_%E4%B8%89%E7%A7%8D%20Non-blocking%20Progress%20Guarantees%EF%BC%88%E8%BF%9B%E5%BA%A6%E4%BF%9D%E8%AF%81%EF%BC%89%E6%A6%82%E8%A7%88/index.md)
