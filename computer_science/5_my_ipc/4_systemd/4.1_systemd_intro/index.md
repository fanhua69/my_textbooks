# 4.1 systemd 命令详解：Linux 服务与系统管理
**介绍**: **systemd Commands: Linux Service and System Management**

## 1. systemd 是什么？

`systemd` 是 Linux 系统中主流的初始化系统和服务管理器（Init System and Service Manager）。

它通常是 Linux 启动后的第一个用户空间进程，PID 为 1，负责：

- 系统启动（System Boot）
- 服务管理（Service Management）
- 进程监督（Process Supervision）
- 系统日志（System Logging）
- Socket 激活（Socket Activation）
- 定时任务（Timer Units）
- 挂载管理（Mount Management）
- 系统关机与重启（Shutdown and Reboot）

查看 PID 1：

```bash
ps -p 1 -o pid,comm,args
```

查看 systemd 版本：

```bash
systemd --version
```

检查 systemd 是否作为 PID 1 运行：

```bash
systemctl is-system-running
```

## 2. systemd 的核心概念：Unit

systemd 使用 Unit（单元）管理系统资源。

Unit 是 systemd 管理对象的基本抽象，可以代表服务、挂载点、设备、Socket、定时器等。

### 2.1 常见 Unit 类型

| 类型 | 后缀 | 作用 |
|---|---|---|
| Service | `.service` | 管理后台服务 |
| Socket | `.socket` | Socket 激活 |
| Target | `.target` | 组织多个 Unit |
| Timer | `.timer` | 定时任务 |
| Mount | `.mount` | 文件系统挂载 |
| Automount | `.automount` | 自动挂载 |
| Device | `.device` | 设备管理 |
| Path | `.path` | 监控文件或目录变化 |
| Slice | `.slice` | 资源管理与分组 |
| Scope | `.scope` | 管理外部创建的进程组 |

例如：

```bash
systemctl status ssh.service
systemctl status cron.service
systemctl list-units --type=service
```

`.service` 是 Unit 文件类型之一，不是 Linux 可执行程序。

### 2.2 Unit 文件存放位置

常见位置：

| 目录 | 用途 |
|---|---|
| `/etc/systemd/system/` | 管理员创建或覆盖的系统 Unit |
| `/run/systemd/system/` | 运行期间生成的 Unit |
| `/usr/lib/systemd/system/` | 软件包提供的系统 Unit |
| `/lib/systemd/system/` | 某些发行版使用的软件包 Unit 目录 |
| `~/.config/systemd/user/` | 用户级 Unit |

注意：不同 Linux 发行版的目录布局可能不同。

查看某个服务的实际 Unit 文件：

```bash
systemctl cat ssh.service
```

查看 Unit 文件路径：

```bash
systemctl show ssh.service -p FragmentPath
```

## 3. systemctl：最重要的管理命令

`systemctl` 是与 systemd 交互的主要命令行工具。

### 3.1 查看服务状态

```bash
systemctl status nginx
```

输出通常包含：

- Loaded：Unit 是否加载，以及是否启用
- Active：当前运行状态
- Main PID：主进程 PID
- Tasks：任务数量
- Memory：内存使用情况
- CPU：CPU 使用情况
- Logs：近期日志

常见状态：

| 状态 | 含义 |
|---|---|
| active (running) | 正在运行 |
| active (exited) | 已完成启动任务，但没有持续运行的主进程 |
| inactive (dead) | 当前未运行 |
| failed | 启动或运行失败 |
| activating | 正在启动 |
| deactivating | 正在停止 |

### 3.2 启动、停止和重启

```bash
# 启动
sudo systemctl start nginx

# 停止
sudo systemctl stop nginx

# 重启
sudo systemctl restart nginx

# 尝试重新加载配置，不重启主进程
sudo systemctl reload nginx

# 如果支持 reload，否则重启
sudo systemctl reload-or-restart nginx
```

`reload` 是否有效，取决于服务是否实现了相应的配置重新加载机制。

### 3.3 开机启动管理

```bash
# 设置开机自动启动
sudo systemctl enable nginx

# 取消开机自动启动
sudo systemctl disable nginx

# 设置开机启动，并立即启动
sudo systemctl enable --now nginx

# 取消开机启动，并立即停止
sudo systemctl disable --now nginx
```

注意：

- `start`：控制当前运行状态。
- `enable`：控制未来启动时是否自动启动。
- 两者是不同的概念。

### 3.4 查看是否启用

```bash
systemctl is-enabled nginx
```

可能返回：

- enabled
- disabled
- static
- masked
- indirect

查看是否正在运行：

```bash
systemctl is-active nginx
```

### 3.5 禁止服务启动

```bash
sudo systemctl mask nginx
```

`mask` 会通过创建指向 `/dev/null` 的链接，使 Unit 无法正常启动。

解除：

```bash
sudo systemctl unmask nginx
```

与 `disable` 的区别：

- disable：不再通过正常的 enable 机制自动启动，但仍可以手动启动。
- mask：阻止该 Unit 被正常启动，包括手动启动。

## 4. 查询和管理 Unit

### 4.1 列出所有已加载 Unit

```bash
systemctl list-units
```

只看 Service：

```bash
systemctl list-units --type=service
```

包含未运行的已加载服务：

```bash
systemctl list-units --type=service --all
```

### 4.2 列出所有已安装的 Service Unit 文件

```bash
systemctl list-unit-files --type=service
```

区别：

- `list-units`：查看当前已加载的 Unit 及其运行状态。
- `list-unit-files`：查看系统中安装的 Unit 文件及其启用状态。

### 4.3 查看失败的服务

```bash
systemctl --failed
```

查看失败的 Unit：

```bash
systemctl list-units --failed
```

清除失败状态：

```bash
sudo systemctl reset-failed
```

这只是清除失败标记，不会自动修复服务。

### 4.4 查看服务依赖

```bash
systemctl list-dependencies nginx
```

查看反向依赖：

```bash
systemctl list-dependencies --reverse nginx
```

查看 Unit 的详细属性：

```bash
systemctl show nginx
```

查看指定属性：

```bash
systemctl show nginx -p MainPID
systemctl show nginx -p ActiveState
systemctl show nginx -p SubState
systemctl show nginx -p Restart
```

## 5. journalctl：查看系统日志

`journalctl` 是 systemd journal 日志系统的查询工具。

它可以查询：

- 系统启动日志
- 服务日志
- 内核日志
- 用户级服务日志
- 特定时间范围内的日志

### 5.1 查看全部日志

```bash
journalctl
```

实时跟踪日志：

```bash
journalctl -f
```

类似于：

```bash
tail -f /var/log/syslog
```

但 journalctl 直接查询 systemd journal，并不要求日志必须写入普通文本文件。

### 5.2 查看指定服务日志

```bash
journalctl -u nginx
```

实时查看：

```bash
journalctl -u nginx -f
```

只看最近 100 行：

```bash
journalctl -u nginx -n 100
```

查看本次启动以来的服务日志：

```bash
journalctl -u nginx -b
```

### 5.3 按时间查询

```bash
# 今天的日志
journalctl --since today

# 最近一小时
journalctl --since "1 hour ago"

# 指定时间范围
journalctl --since "2026-11-23 10:00:00" \
           --until "2026-11-23 11:00:00"
```

### 5.4 查看上一次启动的日志

```bash
journalctl -b -1
```

参数：

- `-b`：当前启动周期。
- `-b -1`：上一次启动周期。
- `-b -2`：上上次启动周期。

查看历史启动记录：

```bash
journalctl --list-boots
```

### 5.5 查看内核日志

```bash
journalctl -k
```

实时跟踪内核日志：

```bash
journalctl -k -f
```

### 5.6 按优先级过滤

```bash
journalctl -p err
```

常见日志级别：

| 级别 | 含义 |
|---|---|
| emerg | 系统不可用 |
| alert | 必须立即处理 |
| crit | 严重错误 |
| err | 错误 |
| warning | 警告 |
| notice | 重要通知 |
| info | 一般信息 |
| debug | 调试信息 |

查看错误及更严重级别：

```bash
journalctl -p err..emerg
```

## 6. 创建自己的 systemd Service

这是 C++ 后台服务开发中非常重要的内容。

假设我们编写了一个 C++ 服务程序：

```bash
/usr/local/bin/my_service
```

我们希望：

1. 开机自动启动。
2. 程序崩溃后自动重启。
3. 由 systemd 监督进程。
4. 可以通过 journalctl 查看日志。

### 6.1 创建 Service Unit 文件

创建：

```bash
sudo vim /etc/systemd/system/my_service.service
```

内容：

```ini
[Unit]
Description=My C++ Background Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/my_service

Restart=on-failure
RestartSec=5

User=myuser
Group=myuser

WorkingDirectory=/var/lib/my_service

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 6.2 Unit 文件各部分的作用

#### [Unit]

描述服务及其启动依赖。

```ini
[Unit]
Description=My C++ Background Service
After=network.target
```

- `Description`：服务描述。
- `After`：启动顺序约束。
- `Wants`：弱依赖。
- `Requires`：强依赖。

注意：`After=` 只约束启动顺序，不代表自动启动所依赖的服务。需要依赖服务时，还要考虑 `Wants=` 或 `Requires=`。

#### [Service]

定义服务进程的运行方式。

```ini
[Service]
Type=simple
ExecStart=/usr/local/bin/my_service
Restart=on-failure
RestartSec=5
```

常见 Type：

| Type | 含义 |
|---|---|
| simple | 默认类型之一，直接运行主进程 |
| exec | 确认执行程序成功后才认为启动完成 |
| forking | 程序启动后自行 fork 到后台 |
| oneshot | 执行一次性任务 |
| notify | 程序通过通知机制告知启动完成 |
| idle | 延迟启动，等待其他任务完成 |

对于现代 C++ 后台服务，通常优先考虑 `simple` 或 `exec`，而不是让程序自行 daemonize。

#### Restart

控制服务退出后的重启行为。

| 配置 | 含义 |
|---|---|
| no | 不自动重启 |
| always | 总是重启 |
| on-success | 正常退出时重启 |
| on-failure | 异常退出时重启 |
| on-abnormal | 信号异常或超时等情况下重启 |
| on-abort | 非正常信号退出时重启 |

例如：

```ini
Restart=on-failure
RestartSec=5
```

表示服务异常退出后，等待 5 秒再尝试重启。

#### [Install]

定义 enable 时的安装关联关系。

```ini
[Install]
WantedBy=multi-user.target
```

表示启用服务时，将它关联到 `multi-user.target`。

### 6.3 加载并启动服务

修改 Unit 文件后：

```bash
# 重新加载 Unit 配置
sudo systemctl daemon-reload

# 设置开机启动
sudo systemctl enable my_service

# 启动
sudo systemctl start my_service

# 查看状态
systemctl status my_service
```

也可以直接：

```bash
sudo systemctl enable --now my_service
```

注意：`daemon-reload` 是让 systemd 重新读取 Unit 文件，不等于让服务程序重新加载自身配置。

### 6.4 修改服务配置后如何处理？

```bash
sudo systemctl daemon-reload
sudo systemctl restart my_service
```

两步分别负责：

1. systemd 重新读取 Unit 文件。
2. 重新启动服务进程。

## 7. systemd 的进程监督与故障恢复

systemd 不只是启动程序，还可以监督服务进程。

### 7.1 自动重启

```ini
[Service]
Restart=on-failure
RestartSec=3
```

当服务异常退出时，systemd 会尝试重新启动它。

### 7.2 限制重启频率

```ini
[Unit]
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Restart=on-failure
RestartSec=3
```

在指定时间窗口内，如果启动次数超过限制，systemd 会停止继续尝试启动，服务可能进入 failed 状态。

### 7.3 进程退出与信号处理

停止服务：

```bash
sudo systemctl stop my_service
```

systemd 默认通常先发送 SIGTERM，等待进程退出；如果超过停止超时时间，再根据配置采取进一步终止措施。

可以配置：

```ini
[Service]
KillSignal=SIGTERM
TimeoutStopSec=30
```

C++ 服务应该正确处理 SIGTERM，完成必要的清理工作：

- 停止接收新任务。
- 通知工作线程退出。
- 等待工作线程结束。
- 刷新日志。
- 释放资源。
- 正常退出。

## 8. systemd 的资源管理

systemd 可以利用 Linux Control Groups（cgroups）管理服务的资源。

例如：

```ini
[Service]
CPUQuota=50%
MemoryMax=512M
TasksMax=100
```

含义：

| 配置 | 作用 |
|---|---|
| CPUQuota | 限制 CPU 使用配额 |
| MemoryMax | 限制内存使用量 |
| TasksMax | 限制进程和线程数量 |

查看服务资源使用情况：

```bash
systemctl status my_service
systemd-cgtop
```

这些机制对于运行大量 C++ 微服务的 Linux 服务器非常有用。

## 9. systemd Timer：替代传统 Cron 的定时任务

systemd 可以使用 `.timer` Unit 实现定时任务。

例如，每天凌晨 2 点执行一次备份程序。

创建：

`/etc/systemd/system/backup.service`

```ini
[Unit]
Description=Daily Backup

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup
```

创建：

`/etc/systemd/system/backup.timer`

```ini
[Unit]
Description=Run Backup Daily

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

启用：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
```

查看定时任务：

```bash
systemctl list-timers
```

`Persistent=true` 表示如果系统关机错过了计划执行时间，在下次启动后可以补执行一次。

## 10. systemd 与传统 SysV Init 的区别

Linux 早期常用 SysV Init 管理启动流程。

systemd 是更现代的系统管理方案。

| 对比 | SysV Init | systemd |
|---|---|---|
| 服务管理 | init 脚本 | Unit |
| 启动方式 | 传统顺序脚本 | 依赖关系与并行启动 |
| 服务监督 | 相对有限 | 原生支持 |
| 日志管理 | 通常依赖 syslog | 可集成 journald |
| 资源管理 | 通常需要额外工具 | 集成 cgroups |
| 定时任务 | cron | cron 或 systemd timer |
| Socket Activation | 不具备原生统一机制 | 支持 |

systemd 的一个重要优势是能够通过依赖关系组织启动过程，并在满足条件时并行启动多个服务。

## 11. Linux 服务故障排查实战

假设一个 C++ 服务无法正常启动。

推荐按以下步骤排查。

### Step 1：查看服务状态

```bash
systemctl status my_service
```

重点关注：

- 是否为 failed。
- Main PID 是否存在。
- Exit Code 是多少。
- 是否存在启动超时。

### Step 2：查看详细日志

```bash
journalctl -u my_service -n 200 --no-pager
```

### Step 3：查看 Unit 配置

```bash
systemctl cat my_service
```

### Step 4：检查进程

```bash
ps aux | grep my_service
```

### Step 5：检查端口

```bash
ss -lntp
```

### Step 6：检查依赖库

```bash
ldd /usr/local/bin/my_service
```

### Step 7：检查 Unit 文件语法

```bash
systemd-analyze verify \
    /etc/systemd/system/my_service.service
```

### Step 8：检查启动耗时

```bash
systemd-analyze blame
```

查看启动依赖关系：

```bash
systemd-analyze critical-chain
```

## 12. 常用命令速查表

| 命令 | 作用 |
|---|---|
| `systemctl status NAME` | 查看服务状态 |
| `systemctl start NAME` | 启动服务 |
| `systemctl stop NAME` | 停止服务 |
| `systemctl restart NAME` | 重启服务 |
| `systemctl reload NAME` | 重新加载服务配置 |
| `systemctl enable NAME` | 设置开机启动 |
| `systemctl disable NAME` | 取消开机启动 |
| `systemctl enable --now NAME` | 启用并立即启动 |
| `systemctl is-active NAME` | 检查是否运行 |
| `systemctl is-enabled NAME` | 检查是否启用 |
| `systemctl --failed` | 查看失败的 Unit |
| `systemctl daemon-reload` | 重新加载 Unit 文件 |
| `systemctl cat NAME` | 查看 Unit 文件 |
| `systemctl show NAME` | 查看 Unit 属性 |
| `systemctl list-units` | 列出已加载 Unit |
| `systemctl list-unit-files` | 列出 Unit 文件 |
| `journalctl -u NAME` | 查看服务日志 |
| `journalctl -u NAME -f` | 实时跟踪服务日志 |
| `journalctl -b` | 查看本次启动日志 |
| `journalctl -b -1` | 查看上次启动日志 |
| `systemctl list-timers` | 查看定时任务 |
| `systemd-analyze blame` | 分析启动耗时 |
| `systemd-cgtop` | 查看 cgroup 资源使用 |

## 13. 总结

systemd 是现代 Linux 系统管理的重要基础设施。

对于 C++ 系统工程师，尤其需要掌握：

1. 使用 systemctl 管理后台服务。
2. 编写 `.service` Unit 文件。
3. 使用 journalctl 分析生产环境日志。
4. 使用 Restart 实现进程故障恢复。
5. 使用 cgroups 管理 CPU、内存和线程资源。
6. 正确处理 SIGTERM，实现优雅退出。
7. 使用 systemd-analyze 分析系统启动性能。

**核心认识：**

systemd 不只是一个启动程序的工具，它是 Linux 用户空间的服务管理、进程监督、日志和资源管理基础设施。

对于生产环境中的 C++ 服务，systemd 通常是服务生命周期管理的重要组成部分。


---

## 导航

- **上一层**：[基础隔离与安全加固项](../index.md)
- **前一节**：[查看系统域下某个守护进程的详细状态](../../3_launchd/index.md)


- **后一节**：[6 Cross-Platform Inter-Process Communication (IPC) Engineering](../../../6_ipc/index.md)
