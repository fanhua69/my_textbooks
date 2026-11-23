# 1.1.1.6 可运行 C++ 示例：共享地址空间、TLS 与同步协作对比

> **简介**：下面提供一个可编译运行的 C++17 示例，直观展示： 1. 同一进程内多线程共享全局/堆状态，而各自拥有独立的 `thread_local` 实例； 2. 通过 `std::atomic` 协调工作线程进度，避免在未同步状态下跨线程读取已结束线程的 `thread_local` 地址。

---

下面提供一个可编译运行的 C++17 示例，直观展示：
1. 同一进程内多线程共享全局/堆状态，而各自拥有独立的 `thread_local` 实例；
2. 通过 `std::atomic` 协调工作线程进度，避免在未同步状态下跨线程读取已结束线程的 `thread_local` 地址。

```cpp
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

struct SharedMetrics {
    std::atomic<uint64_t> completed_tasks{0};
    std::atomic<uint64_t> total_work_units{0};
};

// 每个线程拥有独立的 tls_local_accumulator 实例
thread_local uint64_t tls_local_accumulator = 0;

void worker_fn(int tid, int iterations, SharedMetrics& metrics) {
    for (int i = 0; i < iterations; ++i) {
        // 1. 先在线程局部存储（TLS）中累加，避免高频争用共享原子变量
        tls_local_accumulator += static_cast<uint64_t>(tid + 1);
    }

    // 2. 阶段汇总时再通过原子操作发布到共享状态
    metrics.total_work_units.fetch_add(tls_local_accumulator, std::memory_order_relaxed);
    metrics.completed_tasks.fetch_add(1, std::memory_order_release);

    std::cout << "[Worker " << tid << "] "
              << "tls_local_accumulator=" << tls_local_accumulator
              << ", tls_addr=" << static_cast<const void*>(&tls_local_accumulator)
              << ", shared_addr=" << static_cast<const void*>(&metrics.total_work_units)
              << "\n";
}

int main() {
    constexpr int num_threads = 4;
    constexpr int iterations = 100000;

    SharedMetrics metrics;
    std::vector<std::thread> pool;
    pool.reserve(num_threads);

    for (int t = 0; t < num_threads; ++t) {
        pool.emplace_back(worker_fn, t, iterations, std::ref(metrics));
    }

    for (auto& th : pool) {
        th.join();
    }

    std::cout << "All workers joined. completed_tasks="
              << metrics.completed_tasks.load(std::memory_order_acquire)
              << ", total_work_units="
              << metrics.total_work_units.load(std::memory_order_acquire)
              << "\n";
    return 0;
}
```


---

## 导航

- **上一层**：[1.1.1 进程、线程与共享内存模型 process thread and shared memory](../index.md)
- **前一节**：[1.1.1.5 历史演进、系统差异与工程对比](../1.1.1.5_历史演进、系统差异与工程对比/index.md)
- **后一节**：[1.1.2 数据竞争、竞态条件与线程安全  data race race condition and thread safety](../../1.1.2_数据竞争、竞态条件与线程安全_data_race_race_condition_and_thread_safety/index.md)
