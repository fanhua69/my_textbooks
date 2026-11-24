# 1.5.2.1 控制块 + T 对象存储空间合并为单次内存分配

**介绍**: 控制块 + T 对象存储空间合并为单次内存分配

---
这句话讲的是 C++ 中创建 std::shared_ptr<T> 时，使用 std::make_shared 或 std::allocate_shared 相比直接 std::shared_ptr<T>(new T(args...)) 的底层内存布局与性能优势。

1. 先搞懂两个组成部分
std::shared_ptr 管理对象时，背后通常有两部分数据：

对象 T 本身：你实际要创建的对象（通过 args... 完美转发构造）。

控制块（Control Block）：用于管理生命周期的元数据，通常包含强引用计数（use_count）、弱引用计数（weak_count）、自定义删除器（deleter）或分配器（allocator）等。

对比两种写法：

分开分配（如 std::shared_ptr<T>(new T(args...))）：

先 new T(args...) 在堆上分配一次内存构造 T；

shared_ptr 构造函数再在堆上分配第二次内存创建控制块。
两块内存在堆上位置不一定挨着。

合并为单次分配（make_shared / allocate_shared）：
一次性向内存分配器申请一块足够大的连续内存，把控制块和 T 对象放在同一块内存里，并在原地构造 T。

2. “减少一次分配开销”是什么意思？
堆内存分配（底层常涉及 malloc / operator new）并不是免费的：

分配器需要维护空闲链表/内存池，多线程下还可能涉及锁竞争或线程本地缓存操作。

分配次数越少，CPU 耗费在内存管理上的时间越少，内存碎片风险也更低。

同时，make_shared 在一步内完成分配和构造，还能避免某些复杂表达式下因求值顺序导致的潜在内存泄漏问题。

3. “缓存局部性更好”是什么意思？
CPU 访问内存时，不是按单个字节读的，而是按缓存行（Cache Line，通常为 64 字节）成块加载到 L1/L2/L3 缓存中：

当控制块和 T 对象紧挨在同一块连续内存时，读取/修改引用计数或访问对象成员时，更容易顺带把相邻数据加载进同一条 Cache Line。

相比分散在堆上两个角落的两块内存，Cache Miss（缓存未命中）的概率更低，访存速度更快。

4. make_shared 和 allocate_shared 有什么区别？
std::make_shared<T>(args...)：使用默认的全局内存分配机制（底层通常是 ::operator new）来申请这块合并后的内存。

std::allocate_shared<T>(alloc, args...)：额外传入一个自定义分配器 alloc（例如内存池分配器、对齐分配器、追踪内存用的分配器），用 alloc 来完成这次合并分配与后续回收。

补充一个小代价（面试/工程常见注意点）
合并分配虽然快，但有一个连带特性需要注意：

当最后一个 shared_ptr 析构时，T 的析构函数会立即执行；

但由于控制块和 T 在同一块内存里，如果此时还有 std::weak_ptr 指向它，整块内存必须等最后一个 weak_ptr 也销毁后才能真正归还给分配器（如果 T 本身非常大且 weak_ptr 存活很久，这点需要留意）。
## 导航

- **上一层**：[父级](../index.md)
- **前一节**：[1.5.1 unique_pointer](../../1.5.1_unique_pointer/index.md)
- **后一节**：[1.5.2.2 标准库实现合并T 和control block分配](../1.5.2.2_标准库实现合并T_和control_block分配/index.md)
