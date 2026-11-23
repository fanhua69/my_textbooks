## `systemd` 简介

 **`systemd`** 是现代主流 **Linux 发行版**（如 Ubuntu、Debian、Fedora、RHEL 等）上的**系统与服务管理器（System and Service Manager）**，在系统引导时通常作为 **PID 1** 运行，接管早期初始化、服务编排、守护进程生命周期管理以及日志/设备/会话等系统级子系统。

在架构定位上，它可以类比为 macOS 的 **`launchd`**，但设计目标与子系统生态更贴合 Linux 内核与用户态守护进程模型。

---

### 1. `systemd` 的核心职责与设计特点

- **系统引导与并行启动**：接替传统顺序执行的 SysV init 脚本，通过 **Socket 激活（Socket Activation）**、**D-Bus 激活**与**依赖声明**实现服务并行启动，加快启动速度并降低启动时序耦合。
- **统一 Unit 模型管理资源**：把系统管理对象抽象为声明式的配置文件（Unit），常见类型包括：
  - **`.service`**：后台守护进程或一次性任务；
  - **`.socket`**：监听 TCP/UDP 或 `AF_UNIX` 套接字，支持按需拉起对应服务；
  - **`.timer`**：替代或补充传统 `cron`，支持单调时钟与日历触发；
  - **`.target`**：用于分组 Unit 与表达系统状态里程碑（如 `multi-user.target`、`graphical.target`）；
  - **`.mount` / `.automount` / `.path` / `.slice`**：分别用于挂载点、自动挂载、路径监听以及资源控制分组。
- **基于 `cgroup` 追踪进程树与资源限制**：传统守护进程通过 `double-fork` 脱离终端后，PID 追踪容易丢；`systemd` 依托 Linux `cgroup` 精确追踪整个进程组/服务树，确保停止或重启服务时不会遗留孤儿进程，并可施加 CPU、内存（如 `MemoryMax`）、IO 与进程数限制。
- **结构化日志（`journald`）**：捕获服务标准输出/错误（`stdout` / `stderr`）、内核消息与系统日志，附带元数据，支持按 Unit、时间窗口与优先级检索。

---

### 2. `systemd` 与 IPC / 本地服务的协作方式

在 Linux 系统中，后台守护进程与进程间通信（IPC）常与 `systemd` 深度结合：

1. **Socket Activation（套接字激活）**：
   - 先由 `systemd` 创建并监听 `AF_UNIX` 套接字或网络端口；
   - 当首个客户端连接到达时，`systemd` 启动目标 `.service` 并将已建立监听的 socket 文件描述符传给它；
   - 既实现了**按需启动**，又避免了客户端因服务端尚未就绪而连接失败。
2. **System Bus 与 User Bus 托管**：
   - 在 Linux 桌面与系统服务中，`systemd` 配合 **D-Bus** 管理全局系统总线与每个登录用户的会话总线，支撑服务发现、状态广播与权限策略。
3. **特权隔离与沙盒化**：
   - 可在 `.service` 中配置独立用户/组、私有 `/tmp`、只读系统目录、能力裁剪（Capabilities）与系统调用过滤等隔离参数，缩小服务被攻破后的影响面。

---

### 3. 典型 Unit 文件示例（`.service`）

下面是一个简洁的 Linux 后台服务 Unit 示例，展示依赖声明、执行命令、重启策略与基本安全隔离：

```ini
[Unit]
Description=Example Background Worker Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=worker
Group=worker
ExecStart=/usr/local/bin/example-worker --config /etc/example-worker/config.toml
Restart=on-failure
RestartSec=3s

# 基础隔离与安全加固项
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/lib/example-worker

[Install]
WantedBy=multi-user.target
```

## 4. 日常运维与排查常用命令（systemctl / journalctl）
```Bash
# 查看某个服务的运行状态、主进程 PID 与最近日志
systemctl status example-worker.service

# 重新加载 Unit 文件修改、启动/重启/停止与设置开机自启
systemctl daemon-reload
systemctl restart example-worker.service
systemctl enable example-worker.service

# 查看指定服务的实时与历史结构化日志
journalctl -u example-worker.service -f
journalctl -u example-worker.service --since "1 hour ago"
```

## 5. 工程实践中的常见坑点

Type 与前台运行语义不匹配：Type=simple 期望主进程保持在前台持续运行；若程序内部自行 fork 退到后台却配成 Type=simple，systemd 会误判主进程已退出。

非交互运行环境：服务启动时没有交互式 Shell 环境，依赖的环境变量应在 Unit 文件中显式设置（如 Environment= 或 EnvironmentFile=），路径尽量写绝对路径。

System 实例与 User 实例区分：系统级服务由 root 管理的 systemd 实例维护（通常在 /etc/systemd/system/）；用户会话级服务可通过 systemctl --user 管理（通常在 ~/.config/systemd/user/）。

---

## 目录

- [systemd 命令详解：Linux 服务与系统管理](4.1_systemd_intro/index.md)

## 导航

- **上一层**：[5_my_ipc](../index.md)
- **前一节**：[查看系统域下某个守护进程的详细状态](../3_launchd/index.md)