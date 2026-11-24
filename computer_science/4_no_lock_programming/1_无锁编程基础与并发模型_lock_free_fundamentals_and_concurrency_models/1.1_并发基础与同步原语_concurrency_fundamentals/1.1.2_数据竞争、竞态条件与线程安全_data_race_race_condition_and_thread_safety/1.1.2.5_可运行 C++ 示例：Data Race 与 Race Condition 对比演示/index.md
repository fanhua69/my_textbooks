# 1.1.2.5 可运行 C++ 示例：Data Race 与 Race Condition 对比演示

**介绍**: > **简介**：下面提供一段可编译运行的 C++17 示例，对比展示：

---

下面提供一段可编译运行的 C++17 示例，对比展示：

1. **无同步的共享计数器写操作**：存在 Data Race（UB），仅作反面原理对照（实际工程中应避免）；
2. **原子自增（`fetch_add`）**：消除 Data Race，保证单次累加的原子性；
3. **Check-Then-Act（先检查后扣减）**：即便底层使用 `std::atomic`，若“检查余额是否充足”与“扣减余额”拆成两次独立原子操作，依然会出现 Race Condition（超扣）。

```cpp
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

struct Account {
    std::atomic<int> balance{100};
};

// 反面示例：无同步的共享变量读写存在 Data Race（属于 C++ UB，仅作概念对比）
void unsafe_increment(int& counter, int loops) {
    for (int i = 0; i < loops; ++i) {
        ++counter;
    }
}

// 正确消除 Data Race：使用 std::atomic 保证单次累加的原子性
void atomic_increment(std::atomic<int>& counter, int loops) {
    for (int i = 0; i < loops; ++i) {
        counter.fetch_add(1, std::memory_order_relaxed);
    }
}

// 演示 Race Condition：虽然 balance 是 std::atomic，但“检查 + 扣款”不是原子的，
// 多线程并发调用时可能出现余额被扣成负数的情况。
void buggy_withdraw(Account& acct, int amount) {
    if (acct.balance.load(std::memory_order_acquire) >= amount) {
        // 模拟此处发生线程调度切换，其他线程可能在此期间完成扣款
        std::this_thread::yield();
        acct.balance.fetch_sub(amount, std::memory_order_acq_rel);
    }
}

// 使用 CAS 循环将“检查 + 扣款”合并为原子状态转移，消除 Race Condition
bool safe_withdraw(Account& acct, int amount) {
    int current = acct.balance.load(std::memory_order_acquire);
    while (true) {
        if (current < amount) {
            return false;
        }
        if (acct.balance.compare_exchange_weak(
                current,
                current - amount,
                std::memory_order_acq_rel,
                std::memory_order_acquire)) {
            return true;
        }
        // 若期间被其他线程修改，current 会被自动更新为最新值，循环重试
    }
}

int main() {
    constexpr int threads_n = 4;
    constexpr int loops = 50000;

    std::atomic<int> atomic_counter{0};
    std::vector<std::thread> inc_threads;
    for (int i = 0; i < threads_n; ++i) {
        inc_threads.emplace_back(atomic_increment, std::ref(atomic_counter), loops);
    }
    for (auto& t : inc_threads) {
        t.join();
    }
    std::cout << "atomic_counter = " << atomic_counter.load()
              << " (expected " << threads_n * loops << ")\n";

    // 演示 Check-Then-Act 竞态条件
    Account buggy_acct;
    buggy_acct.balance.store(100);
    std::vector<std::thread> w1;
    for (int i = 0; i < 4; ++i) {
        w1.emplace_back(buggy_withdraw, std::ref(buggy_acct), 60);
    }
    for (auto& t : w1) {
        t.join();
    }
    std::cout << "buggy_acct balance after four 60-withdrawals = "
              << buggy_acct.balance.load() << " (may be negative due to race condition)\n";

    // 演示 CAS 原子状态转移
    Account safe_acct;
    safe_acct.balance.store(100);
    std::vector<std::thread> w2;
    for (int i = 0; i < 4; ++i) {
        w2.emplace_back([&safe_acct]() {
            safe_withdraw(safe_acct, 60);
        });
    }
    for (auto& t : w2) {
        t.join();
    }
    std::cout << "safe_acct balance after four 60-withdrawals = "
              << safe_acct.balance.load() << " (never below 0)\n";

    // 如需对比 unsafe_increment，可取消下方注释并在测试时配合 TSan 观察
    // int plain_counter = 0;
    // (void)unsafe_increment;

    return 0;
}

```


---

## 导航

- **上一层**：[1.1.2 数据竞争、竞态条件与线程安全 data race race condition and thread safety](../index.md)
- **前一节**：[1.1.2.4 历史演进、系统差异与工程对比](../1.1.2.4_历史演进、系统差异与工程对比/index.md)
- **后一节**：[1.1.3 互斥锁、读写锁与自旋锁  mutex rwlock and spinlock](../../1.1.3_互斥锁、读写锁与自旋锁_mutex_rwlock_and_spinlock/index.md)
