# 14.1.1.1 音频回调与实时线程准则

回调中禁止分配、锁、I/O 与系统调用。

## 本节目录

- [14.1.1.1.1 实时安全的代码清单](14.01.1.1.1_实时安全的代码清单_RealtimeSafetyChecklist/index.md)
- [14.1.1.1.2 无锁参数传递与消息队列](14.01.1.1.2_无锁参数传递与消息队列_LockFreeParameterMessaging/index.md)
- [14.1.1.1.3 Core Audio、ALSA 与 JACK 的缓冲与往返延迟](14.01.1.1.3_Core_Audio_ALSA_与_JACK_的缓冲与往返延迟_CoreAudioALSAJACK/index.md)

---

## 导航

← 上一节：[13 电子交易与高频交易系统](../../../../13_电子交易与高频交易系统_ElectronicTradingHFTSystems/index.md)
↑ 返回上级：[14.1.1 实时音频](../index.md)
下一节：[14.1.1.2 音频 DSP 的低延迟实现](../14.01.1.2_音频_DSP_的低延迟实现_LowLatencyDSP/index.md) →
