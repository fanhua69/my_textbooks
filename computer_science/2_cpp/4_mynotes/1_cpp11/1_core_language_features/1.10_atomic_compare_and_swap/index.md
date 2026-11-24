# 1.10 `std::atomic`：`compare_exchange_weak` 与 `compare_exchange_strong`

**介绍**: 在 `std::atomic` 的 CAS（Compare-And-Swap，比较并交换）操作中，`compare_exchange_weak` 和 `compare_exchange_strong` 的核心差异在于**是否允许“伪失败”（spurious failure）**[cite: 4, 5]。

* **`compare_exchange_strong`**：只要原子变量的当前值**确实等于** `expected`，就**保证**原子地将其更新为 `desired` 并返回 `true`；仅当当前值确实不等于 `expected` 时返回 `false`，并将最新值写回 `expected`。
* **`compare_exchange_weak`**：即使原子变量的当前值**等于** `expected`，也**允许**偶发返回 `false`（伪失败），此时不保证修改成功，但会将最新值写回 `expected`（部分实现或硬件场景下需结合实际读值继续重试）[cite: 4]。

---

## 1. 为什么会有“伪失败”？

不同处理器架构实现原子 CAS 的底层机制不同：

* **LL/SC 架构（如 ARM64、PowerPC、RISC-V）**：
  * 常见实现为一对指令（如 ARM64 的 `ldaxr` + `stlxr`）。
  * 在 `ldaxr` 到 `stlxr` 之间，如果目标缓存行被其他核心修改、发生中断、线程切换或缓存争用，`stlxr` 可能失败并返回 `false`，这就是“伪失败”。
  * `compare_exchange_weak` 通常直接映射为单次 LL/SC 尝试；`compare_exchange_strong` 则可能在底层包含内部重试循环，直到确认成功或值确实不匹配。
* **x86 / x86-64 架构**：
  * 底层对应 `LOCK CMPXCHG` 指令，硬件本身就是原子比较并交换，通常不存在 LL/SC 那类因缓存行争用导致的伪失败。
  * 但 C++ 标准语义上仍视 `compare_exchange_weak` 为允许伪失败，跨平台（尤其是 ARM64）代码必须按标准契约编写。

---

## 2. 对比与选型建议

| 维度 | `compare_exchange_weak` | `compare_exchange_strong` |
| :--- | :--- | :--- |
| **真值相等时是否必成功** | 否（允许伪失败返回 `false`） | 是（保证返回 `true`） |
| **适用场景** | 已有 `while` / `for` 重试循环（如无锁结构、`WeakPtr::lock()`）[cite: 4] | 单次 CAS（无外层循环，一次成败决定分支） |
| **ARM64 等 LL/SC 开销** | 少一层内部循环，通常更紧凑/高效 | 内部可能带重试逻辑，略高 |
| **x86-64 开销** | 与 `strong` 相当 | 基准开销 |

---

## 3. 代码示例

### 示例 A：带循环重试 -> 使用 `compare_exchange_weak`

```cpp
#include <atomic>

bool try_increment_if_positive(std::atomic<int>& counter) noexcept {
    int expected = counter.load(std::memory_order_acquire);
    while (expected > 0) {
        if (counter.compare_exchange_weak(
                expected, expected + 1,
                std::memory_order_acq_rel,
                std::memory_order_acquire)) {
            return true;
        }
        // 若发生伪失败或并发修改，expected 已被更新为当前值；若仍 > 0 则继续下一轮
    }
    return false;
}
```


这段代码的目的是：**在多线程并发环境下，安全地将 `counter` 加 `1`，但前提是当前 `counter > 0`**。如果 `counter` 已经变成 `<= 0`（比如引用计数归零、资源已失效/已释放），就放弃加 `1` 并返回 `false`；一旦成功加 `1`，就返回 `true`。

---

## 1. 为什么不能直接写 `counter++` 或 `if (counter > 0) counter++`？

* **直接 `counter++`（或 `fetch_add(1)`）的危险**：如果 `counter` 已经是 `0`，直接加 `1` 会把它从 `0` 变成 `1`，导致已经归零的状态“死灰复燃”。
* **先 `if (counter.load() > 0)` 再 `counter.fetch_add(1)` 的竞态窗口**：
  1. 线程 A 读到 `counter == 1`，判断 `> 0` 成立。
  2. 在线程 A 执行 `+1` 之前，线程 B 把 `counter` 减成了 `0` 并销毁了资源。
  3. 线程 A 醒来继续执行 `+1`，把已经归零的 `counter` 又改成了 `1`，引发严重并发 Bug。

`try_increment_if_positive` 用 **“先读快照 -> 循环校验条件 -> 原子 CAS 确认未变并更新”** 的无锁模式把这个竞态窗口堵死了。

---

## 2. 逐行执行逻辑拆解

```cpp
bool try_increment_if_positive(std::atomic<int>& counter) noexcept {
    int expected = counter.load(std::memory_order_acquire);
    while (expected > 0) {
        if (counter.compare_exchange_weak(
                expected, expected + 1,
                std::memory_order_acq_rel,
                std::memory_order_acquire)) {
            return true;
        }
        // 若发生伪失败或并发修改，expected 已被更新为当前值；若仍 > 0 则继续下一轮
    }
    return false;
}
```

### 第 1 步：读取初始快照
* `int expected = counter.load(std::memory_order_acquire);`
* 先读出 `counter` 当前的值放进局部“期望值” `expected` 中。
* `memory_order_acquire` 保证：如果后续成功拿到这次增量并看到其他线程 `release` 之前的写入，相关的内存可见性顺序不会乱。

### 第 2 步：循环检查“是否仍为正数”
* `while (expected > 0)`
* 只要当前推测的 `expected > 0`，就说明还有机会成功加 `1`，进入循环尝试提交修改；一旦 `expected <= 0`，说明已经没有可递增的正数了，直接跳出 `while` 循环，在第 10 行返回 `false`。

### 第 3 步：原子 CAS 尝试“条件更新”
* `counter.compare_exchange_weak(expected, expected + 1, std::memory_order_acq_rel, std::memory_order_acquire)`
* 这句话在硬件层面做的是原子比较交换：
  * **如果 `counter` 当前值 == `expected`**：说明从我们读 `expected` 到现在，没有别的线程改过 `counter`（前提是没有发生伪失败）。此时原子地把 `counter` 改成 `expected + 1`，并返回 `true`，函数立刻结束返回 `true`。
  * **如果 `counter` 当前值 != `expected`（或发生伪失败）**：
    * 修改失败，返回 `false`。
    * `compare_exchange_weak` 会把 `counter` **最新的实际值**写回 `expected`（注意：表达式 `expected + 1` 只是算出一个临时新值，不会改 `expected` 本身）。
    * 控制流回到 `while (expected > 0)`：
      * 如果新写回的 `expected` 已经变成 `0` 或负数，循环条件不成立，直接返回 `false`。
      * 如果新写回的 `expected` 仍然是 `> 0`（比如别的线程刚从 `2` 改成 `3`，而我们之前看到的是 `2`），循环继续，拿着最新的 `expected` 再试一次。

### 第 4 步：失败出口
* `return false;`
* 只有当 `expected <= 0` 时才会走到这里，表示目标计数已不再大于 `0`，本次递增未发生。

---

## 3. 两种典型并发场景推演

### 场景 A：并发递增成功（`counter` 初值为 `2`）
1. 线程 1 读到 `expected = 2`（`> 0`）。
2. 线程 2 抢先一步把 `counter` 改成了 `3`。
3. 线程 1 执行 `compare_exchange_weak(expected, 3, ...)`：发现 `counter` 实际是 `3 != 2`，CAS 失败，把 `expected` 更新为 `3`。
4. 回到 `while (expected > 0)`：`3 > 0` 仍成立。
5. 线程 1 再次执行 `compare_exchange_weak(expected, 4, ...)`：此时 `counter` 还是 `3 == expected`，CAS 成功，把 `counter` 设为 `4`，返回 `true`。

### 场景 B：并发归零导致失败（`counter` 初值为 `1`）
1. 线程 1 读到 `expected = 1`（`> 0`）。
2. 线程 2 把 `counter` 减成了 `0`。
3. 线程 1 执行 `compare_exchange_weak`：发现 `counter` 实际是 `0 != 1`，CAS 失败，把 `expected` 更新为 `0`。
4. 回到 `while (expected > 0)`：`0 > 0` 为假，退出循环，返回 `false`。

---

## 4. 总结一句话

它就是一个**带条件守卫（`expected > 0`）的无锁 CAS 重试循环**：宁可多试几次、甚至在计数归零时果断放弃，也绝不在 `counter <= 0` 时错误地把计数加回去。



### 示例 B：单次尝试（无循环） -> 使用 `compare_exchange_strong`

```cpp
#include <atomic>

enum class State { Idle, Running };

bool try_start(std::atomic<State>& state) noexcept {
    State expected = State::Idle;
    // 仅尝试一次，避免因伪失败导致状态明明是 Idle 却失败
    return state.compare_exchange_strong(
        expected, State::Running,
        std::memory_order_acq_rel,
        std::memory_order_acquire);
}
```

---

## 4. 注意事项

* **`expected` 是非 `const` 引用**：CAS 失败时，原子变量的最新值会被写回 `expected`；循环中不要在失败后手动把 `expected` 恢复成旧值。
* **内存序参数顺序**：四参数重载中，第 3 个参数是**成功**时的 `std::memory_order`，第 4 个参数是**失败**时的 `std::memory_order`（失败内存序不能强于成功内存序，且不能指定 `release` 或 `acq_rel`）。


---

## 导航

- **上一层**：[1_cpp11](../index.md)
- **前一节**：[1.09 smart pointer](../1.09_smart_pointer/index.md)
- **后一节**：[1.11 C++ 的 std::aligned_storage，以及与它相关的 alignas](../1.11_alignas_storage/index.md)
