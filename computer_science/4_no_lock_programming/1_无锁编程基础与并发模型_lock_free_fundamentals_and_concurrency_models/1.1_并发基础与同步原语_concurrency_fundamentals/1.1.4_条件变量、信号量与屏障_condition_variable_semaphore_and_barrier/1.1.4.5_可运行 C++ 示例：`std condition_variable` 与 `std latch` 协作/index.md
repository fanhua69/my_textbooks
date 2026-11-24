# 1.1.4.5 可运行 C++ 示例：`std::condition_variable` 与 `std::latch` 协作

**介绍**: > **简介**：下面提供一段可编译运行的 C++20 示例，展示使用 `std::latch` 等待所有工作线程就绪，以及使用 `std::mutex` + `std::condition_variable` 实现带谓词防虚假唤醒的线程安全任务队列。

---

下面提供一段可编译运行的 C++20 示例，展示使用 `std::latch` 等待所有工作线程就绪，以及使用 `std::mutex` + `std::condition_variable` 实现带谓词防虚假唤醒的线程安全任务队列。

```cpp
#include <condition_variable>
#include <iostream>
#include <latch>
#include <mutex>
#include <optional>
#include <queue>
#include <thread>
#include <vector>

template <typename T>
class BoundedTaskQueue {
public:
    void push(T item) {
        {
            std::lock_guard<std::mutex> lk(mtx_);
            queue_.push(std::move(item));
        }
        cv_.notify_one();
    }

    std::optional<T> pop() {
        std::unique_lock<std::mutex> lk(mtx_);
        // 使用谓词避免虚假唤醒（Spurious Wakeup）与唤醒丢失竞态
        cv_.wait(lk, [this]() { return !queue_.empty() || stopped_; });

        if (queue_.empty()) {
            return std::nullopt;
        }
        T item = std::move(queue_.front());
        queue_.pop();
        return item;
    }

    void stop() {
        {
            std::lock_guard<std::mutex> lk(mtx_);
            stopped_ = true;
        }
        cv_.notify_all();
    }

private:
    std::mutex mtx_;
    std::condition_variable cv_;
    std::queue<T> queue_;
    bool stopped_{false};
};

int main() {
    constexpr int kWorkers = 3;
    BoundedTaskQueue<int> tasks;
    std::latch ready_latch(kWorkers);

    std::vector<std::thread> workers;
    workers.reserve(kWorkers);
    for (int id = 0; id < kWorkers; ++id) {
        workers.emplace_back([id, &tasks, &ready_latch]() {
            // 模拟线程初始化完成，通知主线程
            ready_latch.arrive_and_wait();

            while (auto item = tasks.pop()) {
                std::cout << "[Worker " << id << "] processed task " << *item << "\n";
            }
        });
    }

    // 等待所有工作线程完成初始化后再投递任务
    ready_latch.wait();
    for (int t = 1; t <= 9; ++t) {
        tasks.push(t);
    }

    tasks.stop();
    for (auto& th : workers) {
        th.join();
    }
    return 0;
}

```


---

## 导航

- **上一层**：[1.1.4 条件变量、信号量与屏障 condition variable semaphore and barrier](../index.md)
- **前一节**：[1.1.4.4 与原子操作的协作关系：阻塞原语 vs. `std::atomic::wait`](../1.1.4.4_%E4%B8%8E%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C%E7%9A%84%E5%8D%8F%E4%BD%9C%E5%85%B3%E7%B3%BB%EF%BC%9A%E9%98%BB%E5%A1%9E%E5%8E%9F%E8%AF%AD%20vs.%20%60std%20atomic%20wait%60/index.md)
- **后一节**：[1.1.5 锁竞争、上下文切换与优先级反转  lock contention context switch and priority inversion](../../1.1.5_锁竞争、上下文切换与优先级反转_lock_contention_context_switch_and_priority_inversion/index.md)
