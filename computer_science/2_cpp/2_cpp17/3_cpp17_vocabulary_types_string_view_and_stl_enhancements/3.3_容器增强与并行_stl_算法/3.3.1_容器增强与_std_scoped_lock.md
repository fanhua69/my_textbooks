# 3.3.1 try_emplace、insert_or_assign、节点句柄（extract / insert / merge）与 std::scoped  lock

**介绍**: 掌握键已存在时不构造值的 try_emplace、存在则赋值/不存在则插入的 insert_or_assign、map/set 节点提取与合并，以及 CTAD 加持的死锁安全多锁封装 std::scoped_lock。

---

## 导航

← 上一节：[3.2 std::string_view、字符串搜索器与 std::invoke / std::apply / as  const](../../3.2_string_view_搜索器与函数调用工具/index.md)
↑ 返回上级：[3.3 关联容器增强（try emplace / insert or assign / 节点提取）与并行 STL](../index.md)
下一节：[3.3.2 并行 STL（std::execution::seq / par / par_unseq）与 reduce / transform  reduce / scan](../3.3.2_并行_stl_执行策略与规约扫描算法/index.md) →
