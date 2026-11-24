# 3.2.1 std::string view 切片/前缀后缀/子串与悬空指针生命周期陷阱

掌握非拥有字符序列视图、substr/remove_prefix/remove_suffix、无结尾 '\0' 保证及避免绑定临时字符串导致的悬空引用。

---

## 导航

← 上一节：[3.1 std::optional、std::variant、std::any 与 std::byte](../../01_optional_variant_any_与_byte/index.md)
↑ 返回上级：[3.2 std::string_view、字符串搜索器与 std::invoke / std::apply / as  const](../index.md)
下一节：[3.2.2 std::invoke、std::apply、std::make from tuple、std::as const 与 Boyer-Moore 搜索器](../02_invoke_apply_as_const_与搜索器/index.md) →
