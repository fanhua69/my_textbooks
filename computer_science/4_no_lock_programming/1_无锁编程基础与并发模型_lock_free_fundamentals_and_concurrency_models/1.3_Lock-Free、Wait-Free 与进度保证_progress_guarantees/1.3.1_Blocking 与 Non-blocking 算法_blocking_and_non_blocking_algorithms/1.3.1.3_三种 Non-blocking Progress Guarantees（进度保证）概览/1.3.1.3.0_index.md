# 1.3.1.3 三种 Non-blocking Progress Guarantees（进度保证）概览

**介绍**: > **简介**：非阻塞并不是一个单一的性能档位，而是一组强度逐级递增的 Progress Guarantees（进度保证）：

---

非阻塞并不是一个单一的性能档位，而是一组强度逐级递增的 **Progress Guarantees（进度保证）**：

$$\text{Wait-Free} \implies \text{Lock-Free} \implies \text{Obstruction-Free}$$

| 进度等级 | 保证谁能取得进展？ | 核心含义 |
| :--- | :--- | :--- |
| **Obstruction-Free（无障碍）** | **独占执行的线程** | 如果某个线程最终能够获得一段不受其他线程干扰的独占执行时间，它就能在有限步内完成操作 |
| **Lock-Free（无锁）** | **至少有一个线程** | 无论线程如何交错执行、甚至部分线程暂停，系统整体总能在有限步内保证至少一个线程完成操作（允许个别线程因冲突重试而饥饿） |
| **Wait-Free（无等待）** | **每一个线程** | 无论调度器如何干扰，**每一个**活跃线程都能在自身有界步数（Bounded Steps）内完成操作，彻底杜绝饥饿 |

以三个线程 `A`、`B`、`C` 并发向共享结构提交更新为例：
- **Obstruction-Free**：`A` 只要拿到一段不被打断的独立执行窗口，就能顺利完成自己的操作；
- **Lock-Free**：`A`、`B`、`C` 相互竞争时，可能 `A` 连续 CAS 失败而发生 **Starvation（饥饿）**，但 `B` 或 `C` 之中至少有一个线程会不断推进成功；
- **Wait-Free**：`A`、`B`、`C` 每个线程各自都保证在有限步数内完成，不会出现某个线程被无限期“饿死”。

---


---

## 导航

- **上一层**：[1.3.1 Blocking 与 Non-blocking 算法  blocking and non blocking algorithms](../index.md)
- **前一节**：[1.3.1.2 Non-blocking 算法与“线程暂停”的本质区别](../1.3.1.2_Non-blocking%20%E7%AE%97%E6%B3%95%E4%B8%8E%E2%80%9C%E7%BA%BF%E7%A8%8B%E6%9A%82%E5%81%9C%E2%80%9D%E7%9A%84%E6%9C%AC%E8%B4%A8%E5%8C%BA%E5%88%AB/index.md)
- **后一节**：[1.3.1.4 C++ 标准库视角与低延迟系统中的现实工程考量](../1.3.1.4_C%2B%2B%20%E6%A0%87%E5%87%86%E5%BA%93%E8%A7%86%E8%A7%92%E4%B8%8E%E4%BD%8E%E5%BB%B6%E8%BF%9F%E7%B3%BB%E7%BB%9F%E4%B8%AD%E7%9A%84%E7%8E%B0%E5%AE%9E%E5%B7%A5%E7%A8%8B%E8%80%83%E9%87%8F/index.md)
