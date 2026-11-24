# 3.2 特殊成员函数、=default/=delete、广义 POD 与内存对齐

掌握编译器隐式生成规则、显式控制特殊成员函数、广义 POD 分类以及 alignof / alignas 底层对齐控制。

## 本节目录

- [3.2.1 =default 与 =delete 显式默认与禁用函数](01_default_与_delete_显式控制函数/index.md)
- [3.2.2 移动特殊成员函数的隐式生成与抑制规则](02_移动特殊成员函数的隐式生成与抑制/index.md)
- [3.2.3 广义 POD（Generalized POD）、平凡类型与标准布局类型](03_广义_pod_平凡类型与标准布局类型/index.md)
- [3.2.4 alignof 运算符与 alignas 对齐说明符](04_alignof_与_alignas_内存对齐控制/index.md)

---

## 导航

← 上一节：[3.1 类定义、成员初始化、委托构造与继承构造](../01_类定义_成员初始化_委托构造与继承构造/index.md)
↑ 返回上级：[3 类、对象生命周期、对齐与继承控制](../index.md)
下一节：[3.3 继承控制、内联命名空间与右角括号语法](../03_override_final_inline_namespace_与右角括号/index.md) →
