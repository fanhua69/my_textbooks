## `launchd` 简介

**`launchd`** 是 **macOS（以及 iOS / iPadOS / tvOS / watchOS）上的核心系统初始化进程与后台服务管理器**，在体系定位上相当于 Linux 中的 `systemd`（或早期的 SysV init）。

它不仅是操作系统内核完成早期初始化后拉起的第一个用户态进程（**PID 1**），也是 **XPC**、**`LaunchDaemon`** 和 **`LaunchAgent`** 能够实现按需启停、端口托管与生命周期管理的底层支柱。

---

### 1. `launchd` 的核心职责

- **系统引导与进程树根节点**：内核启动后拉起 `launchd`（PID 1），由它统一启动、监控并回收后续系统守护进程与用户会话服务。
- **守护进程与代理托管（Daemons & Agents）**：
  - **`LaunchDaemon`**：系统级后台服务，随系统启动，可在无用户登录时运行，通常以 `root` 或指定系统账号执行（plist 常见于 `/Library/LaunchDaemons/`）。
  - **`LaunchAgent`**：用户会话级后台代理，在对应用户登录图形/用户会话时启动，运行在当前用户权限下，可访问用户会话上下文（plist 常见于 `~/Library/LaunchAgents/` 或 `/Library/LaunchAgents/`）。
- **按需启动（On-Demand Activation）**：服务无需开机常驻内存。可通过配置让 `launchd` 代为监听 Mach 服务名、Socket 端口或文件系统路径变化，仅在有客户端请求连接或事件触发时动态拉起进程，空闲时由系统回收。
- **崩溃拉起与生命周期控制**：服务异常退出时，可根据配置（如 `KeepAlive`）自动重启；管理员与开发者可通过 `launchctl` 查询状态、加载/卸载及触发运行。

---

### 2. `launchd` 与 `NSXPCConnection` / IPC 的关系

`NSXPCConnection` 与 `xpc(3)` 之所以在 macOS 上无需手写复杂的服务发现与守护进程拉起逻辑，核心原因就是由 `launchd` 在底层托管：

1. **Mach 服务注册与路由**：服务端在其 `launchd` 的 `.plist` 配置文件中声明 `MachServices` 名称，`launchd` 负责维护 Mach 端口注册表与请求路由。
2. **按需拉起服务端**：客户端通过 `NSXPCConnection` 连接具名 Mach 服务时，若目标 `LaunchDaemon` 或 `XPC Service` 尚未启动，`launchd` 会拦截连接请求并自动拉起服务端进程，随后建立通信通道。
3. **权限与会话隔离**：`LaunchDaemon`（系统域）与 `LaunchAgent`（用户域）天然划分了权限边界，结合 XPC 的 Audit Token 与代码签名（Code Signing）校验，构成了 macOS 标准的特权分离架构。

---

### 3. 常用管理命令（`launchctl`）

现代 macOS 推荐使用 `bootstrap` / `bootout` / `print` / `kickstart` 等子命令管理服务：

```bash
# 查看系统域下某个守护进程的详细状态
launchctl print system/<com.example.daemon.label>

# 查看当前用户图形会话域下的代理状态
launchctl print gui/\$(id -u)/<com.example.agent.label>

# 列出当前域下已加载的服务
launchctl list


---

## 导航

- **上一层**：[5_my_ipc](../index.md)
- **前一节**：[5_my_ipc](../index.md)
- **后一节**：[基础隔离与安全加固项](../2_systemd/index.md)