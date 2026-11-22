# 3.3.2.3 vDSO 与 clock_gettime 的开销

用户态读取时间避免系统调用，及时钟源回退风险。

---

## 导航

← 上一节：[3.3.2.2 nanosleep、clock_nanosleep 与忙等](../03.03.2.2_nanosleep_clock_nanosleep_与忙等_SleepVersusSpin/index.md)
↑ 返回上级：[3.3.2 定时器与时钟](../index.md)
下一节：[3.3.3 系统调用与上下文切换](../../03.03.3_系统调用与上下文切换_SyscallsContextSwitch/index.md) →
