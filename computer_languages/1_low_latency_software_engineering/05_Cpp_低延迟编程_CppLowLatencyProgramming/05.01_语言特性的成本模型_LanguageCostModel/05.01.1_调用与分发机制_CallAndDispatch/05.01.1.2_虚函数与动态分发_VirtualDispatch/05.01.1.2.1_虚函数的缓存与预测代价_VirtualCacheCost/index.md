# 5.1.1.2.1 虚函数的缓存与预测代价

vptr 读取、间接分支误预测与冷启动。

## 本节目录

- [5.1.1.2.1.1 vptr 与 vtable 的缓存行为](05.01.1.2.1.1_vptr_与_vtable_的缓存行为_VptrVtableCache/index.md)
- [5.1.1.2.1.2 间接分支预测失败的代价](05.01.1.2.1.2_间接分支预测失败的代价_IndirectBranchMispredict/index.md)

---

## 导航

← 上一节：[5.1.1.1 内联与调用约定](../../05.01.1.1_内联与调用约定_InliningAndCallingConvention/index.md)
↑ 返回上级：[5.1.1.2 虚函数与动态分发](../index.md)
下一节：[5.1.1.2.2 去虚化与 final 的作用](../05.01.1.2.2_去虚化与_final_的作用_Devirtualization/index.md) →
