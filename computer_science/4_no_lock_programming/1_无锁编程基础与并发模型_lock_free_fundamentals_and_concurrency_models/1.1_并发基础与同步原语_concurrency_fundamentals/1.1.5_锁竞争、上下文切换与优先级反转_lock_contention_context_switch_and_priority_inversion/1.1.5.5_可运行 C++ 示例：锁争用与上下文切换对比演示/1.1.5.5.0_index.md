# 1.1.5.5 可运行 C++ 示例：锁争用与上下文切换对比演示

**介绍**: > **简介**：下面通过一个自包含的 C++17 示例对比高争用共享锁与分片/无争用局部累加在多线程下的耗时差异（可用 `g++ -O2 -std=c++17 -pthread` 编译运行）：

---

下面通过一个自包含的 C++17 示例对比**高争用共享锁**与**分片/无争用局部累加**在多线程下的耗时差异（可用 `g++ -O2 -std=c++17 -pthread` 编译运行）：

```cpp
#include <chrono>
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

template <typename Fn>
double measure_ms(Fn&& fn) {
    auto start = Clock::now();
    fn();
    auto end = Clock::now();
    return std::chrono::duration<double, std::milli>(end - start).count();
}

// 场景 A：多线程高频争用同一把全局互斥锁，制造锁竞争与频繁阻塞/切换
double run_high_contention(int num_threads, int iterations_per_thread) {
    std::mutex mtx;
    long long shared_counter = 0;

    return measure_ms([&]() {
        std::vector<std::thread> workers;
        workers.reserve(num_threads);

        for (int t = 0; t < num_threads; ++t) {
            workers.emplace_back([&, t]() {
                long long local_acc = 0;
                for (int i = 0; i < iterations_per_thread; ++i) {
                    std::lock_guard<std::mutex> lk(mtx);
                    shared_counter += (i + t) & 1;
                    local_acc += 1;
                }
                if (local_acc < 0) {
                    std::cerr << local_acc << "\n";
                }
            });
        }

        for (auto& th : workers) {
            th.join();
        }
    });
}

// 场景 B：减少共享锁争用（先在线程局部累加，仅在汇总阶段加锁一次）
double run_low_contention(int num_threads, int iterations_per_thread) {
    std::mutex mtx;
    long long total_counter = 0;

    return measure_ms([&]() {
        std::vector<std::thread> workers;
        workers.reserve(num_threads);

        for (int t = 0; t < num_threads; ++t) {
            workers.emplace_back([&, t]() {
                long long local_counter = 0;
                for (int i = 0; i < iterations_per_thread; ++i) {
                    local_counter += (i + t) & 1;
                }
                std::lock_guard<std::mutex> lk(mtx);
                total_counter += local_counter;
            });
        }

        for (auto& th : workers) {
            th.join();
        }
    });
}

} // namespace

int main() {
    const unsigned hw = std::thread::hardware_concurrency();
    const int num_threads = static_cast<int>(hw > 0 ? hw : 4);
    const int iterations = 2'000'000;

    std::cout << "Hardware concurrency: " << num_threads
              << ", iterations per thread: " << iterations << "\n";

    double t_high = run_high_contention(num_threads, iterations);
    double t_low = run_low_contention(num_threads, iterations);

    std::cout << "High lock contention time : " << t_high << " ms\n";
    std::cout << "Low lock contention time  : " << t_low << " ms\n";
    return 0;
}
```


---

## 导航

- **上一层**：[1.1.5 锁竞争、上下文切换与优先级反转  lock contention context switch and priority inversion](../index.md)
- **前一节**：[1.1.5.4 诊断指标与工程观测思路](../1.1.5.4_诊断指标与工程观测思路/index.md)
- **后一节**：[1.2 并发拓扑与生产者消费者模型  concurrency topologies](../../../1.2_并发拓扑与生产者消费者模型_concurrency_topologies/index.md)
