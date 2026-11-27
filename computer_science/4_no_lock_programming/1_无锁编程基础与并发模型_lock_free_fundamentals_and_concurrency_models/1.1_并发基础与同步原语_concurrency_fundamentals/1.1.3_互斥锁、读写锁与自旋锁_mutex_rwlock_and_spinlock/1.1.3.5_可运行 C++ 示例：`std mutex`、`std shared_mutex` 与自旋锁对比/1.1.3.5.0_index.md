# 1.1.3.5 可运行 C++ 示例：`std::mutex`、`std::shared_mutex` 与自旋锁对比

**介绍**: > **简介**：下面提供一段可编译运行的 C++17 示例，展示互斥锁、读写锁与基于 `std::atomic_flag` 的自旋锁的基本用法与临界区保护方式。

---

下面提供一段可编译运行的 C++17 示例，展示互斥锁、读写锁与基于 `std::atomic_flag` 的自旋锁的基本用法与临界区保护方式。

```cpp
#include <atomic>
#include <chrono>
#include <iostream>
#include <mutex>
#include <shared_mutex>
#include <thread>
#include <vector>

// 1. 简单的自旋锁（演示原理，实际生产中需结合核心绑定与退避策略评估）
class Spinlock {
public:
    void lock() noexcept {
        while (flag_.test_and_set(std::memory_order_acquire)) {
#if defined(__x86_64__) || defined(_M_X64)
            __builtin_ia32_pause();
#elif defined(__aarch64__) || defined(_M_ARM64)
            __yield();
#else
            std::this_thread::yield();
#endif
        }
    }

    void unlock() noexcept {
        flag_.clear(std::memory_order_release);
    }

private:
    std::atomic_flag flag_ = ATOMIC_FLAG_INIT;
};

// 2. 读多写少场景下的共享配置表（使用 std::shared_mutex）
class ConfigStore {
public:
    uint64_t read_version() const {
        std::shared_lock<std::shared_mutex> lock(rw_mutex_);
        return version_;
    }

    void update_version(uint64_t new_ver) {
        std::unique_lock<std::shared_mutex> lock(rw_mutex_);
        version_ = new_ver;
    }

private:
    mutable std::shared_mutex rw_mutex_;
    uint64_t version_{0};
};

int main() {
    constexpr int kThreads = 4;
    constexpr int kIterations = 50000;

    // A. std::mutex 保护共享计数器
    std::mutex mtx;
    uint64_t mutex_counter = 0;
    std::vector<std::thread> t1;
    for (int i = 0; i < kThreads; ++i) {
        t1.emplace_back([&]() {
            for (int j = 0; j < kIterations; ++j) {
                std::lock_guard<std::mutex> lk(mtx);
                ++mutex_counter;
            }
        });
    }
    for (auto& th : t1) th.join();

    // B. Spinlock 保护极短临界区
    Spinlock spin;
    uint64_t spin_counter = 0;
    std::vector<std::thread> t2;
    for (int i = 0; i < kThreads; ++i) {
        t2.emplace_back([&]() {
            for (int j = 0; j < kIterations; ++j) {
                spin.lock();
                ++spin_counter;
                spin.unlock();
            }
        });
    }
    for (auto& th : t2) th.join();

    // C. std::shared_mutex 演示多读者并发与独占写更新
    ConfigStore store;
    std::vector<std::thread> readers;
    std::atomic<uint64_t> observed_sum{0};
    for (int i = 0; i < kThreads; ++i) {
        readers.emplace_back([&]() {
            uint64_t local = 0;
            for (int j = 0; j < 20000; ++j) {
                local += store.read_version();
            }
            observed_sum.fetch_add(local, std::memory_order_relaxed);
        });
    }
    std::thread writer([&]() {
        for (uint64_t v = 1; v <= 100; ++v) {
            store.update_version(v);
        }
    });

    for (auto& th : readers) th.join();
    writer.join();

    std::cout << "mutex_counter=" << mutex_counter
              << ", spin_counter=" << spin_counter
              << ", final_version=" << store.read_version()
              << ", observed_sum=" << observed_sum.load() << "\n";
    return 0;
}

```


---

## 导航

- **上一层**：[1.1.3 互斥锁、读写锁与自旋锁 mutex rwlock and spinlock](../index.md)
- **前一节**：[1.1.3.4 公平性、饥饿与锁/无锁演进对比](../1.1.3.4_%E5%85%AC%E5%B9%B3%E6%80%A7%E3%80%81%E9%A5%A5%E9%A5%BF%E4%B8%8E%E9%94%81%20%E6%97%A0%E9%94%81%E6%BC%94%E8%BF%9B%E5%AF%B9%E6%AF%94/index.md)
- **后一节**：[1.1.4 条件变量、信号量与屏障 condition variable semaphore and barrier](../../1.1.4_条件变量、信号量与屏障_condition_variable_semaphore_and_barrier/index.md)
