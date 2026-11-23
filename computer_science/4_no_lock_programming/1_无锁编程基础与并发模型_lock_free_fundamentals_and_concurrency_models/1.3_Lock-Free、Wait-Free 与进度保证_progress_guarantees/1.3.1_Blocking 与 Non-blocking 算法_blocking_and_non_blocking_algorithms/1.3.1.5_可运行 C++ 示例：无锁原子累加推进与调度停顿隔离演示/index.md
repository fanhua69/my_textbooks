# 1.3.1.5 可运行 C++ 示例：无锁原子累加推进与调度停顿隔离演示

> **简介**：下面给出一个自包含的 C++20 无锁示例（使用 `std::atomic` 与 `compare_exchange_weak`，不使用 `std::mutex`），演示当某个线程在执行 CAS 更新前发生调度停顿（模拟抢占/延迟）时，其余线程仍能持续推进系统状态，并统计整体与单次推进耗时（可用 `g++ -O2...

---

下面给出一个自包含的 C++20 无锁示例（使用 `std::atomic` 与 `compare_exchange_weak`，不使用 `std::mutex`），演示当某个线程在执行 CAS 更新前发生调度停顿（模拟抢占/延迟）时，其余线程仍能持续推进系统状态，并统计整体与单次推进耗时（可用 `g++ -O2 -std=c++20 -pthread` 编译运行）：

```cpp
#include <algorithm>
#include <atomic>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <thread>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

// 基于无锁 CAS 的共享计数器推进：
// 若某线程在读取旧值后、执行 CAS 前发生调度延迟，其余线程仍可独立完成状态推进。
void run_lock_free_progress_demo(int num_threads, int ops_per_thread) {
    alignas(64) std::atomic<long long> shared_counter{0};
    std::atomic<bool> stall_injected{false};
    std::vector<double> max_step_ms(num_threads, 0.0);

    const auto t0 = Clock::now();
    std::vector<std::thread> workers;
    workers.reserve(num_threads);

    for (int tid = 0; tid < num_threads; ++tid) {
        workers.emplace_back([&, tid]() {
            double local_max_ms = 0.0;
            const int stall_at = ops_per_thread / 3;

            for (int i = 0; i < ops_per_thread; ++i) {
                const auto step_start = Clock::now();

                long long expected = shared_counter.load(std::memory_order_relaxed);
                if (tid == 0 && i == stall_at &&
                    !stall_injected.exchange(true, std::memory_order_relaxed)) {
                    // 模拟线程 0 在提交 CAS 前被调度器暂停 20ms
                    std::this_thread::sleep_for(std::chrono::milliseconds(20));
                }

                while (!shared_counter.compare_exchange_weak(
                    expected, expected + 1,
                    std::memory_order_release,
                    std::memory_order_relaxed)) {
                    // 发生并发修改时，expected 已更新为最新值，在用户态直接重试
                }

                const double step_ms =
                    std::chrono::duration<double, std::milli>(Clock::now() - step_start).count();
                if (step_ms > local_max_ms) {
                    local_max_ms = step_ms;
                }
            }
            max_step_ms[tid] = local_max_ms;
        });
    }

    for (auto& th : workers) {
        th.join();
    }

    const double total_ms =
        std::chrono::duration<double, std::milli>(Clock::now() - t0).count();

    double other_threads_max = 0.0;
    for (int tid = 1; tid < num_threads; ++tid) {
        other_threads_max = std::max(other_threads_max, max_step_ms[tid]);
    }

    std::cout << "Atomic is_always_lock_free : "
              << std::boolalpha << std::atomic<long long>::is_always_lock_free << "\n"
              << "Final counter value        : " << shared_counter.load(std::memory_order_acquire) << "\n"
              << "Total elapsed time         : " << std::fixed << std::setprecision(2) << total_ms << " ms\n"
              << "Other threads max step     : " << std::fixed << std::setprecision(3) << other_threads_max << " ms\n";
}

} // namespace

int main() {
    run_lock_free_progress_demo(4, 150'000);
    return 0;
}
```


---

## 导航

- **上一层**：[1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms](../index.md)
- **前一节**：[1.3.1.4 C++ 标准库视角与低延迟系统中的现实工程考量](../1.3.1.4_C%2B%2B%20%E6%A0%87%E5%87%86%E5%BA%93%E8%A7%86%E8%A7%92%E4%B8%8E%E4%BD%8E%E5%BB%B6%E8%BF%9F%E7%B3%BB%E7%BB%9F%E4%B8%AD%E7%9A%84%E7%8E%B0%E5%AE%9E%E5%B7%A5%E7%A8%8B%E8%80%83%E9%87%8F/index.md)
- **后一节**：[1.3.2 Obstruction-Free：无障碍  obstruction free](../../1.3.2_Obstruction-Free：无障碍_obstruction_free/index.md)
