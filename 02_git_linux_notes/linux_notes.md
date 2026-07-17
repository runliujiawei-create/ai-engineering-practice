# Linux 学习笔记：面向 Python、AI 与服务器开发

> 适用场景：Ubuntu/Linux 服务器、VSCode Remote SSH、Python/Conda、模型训练、FastAPI/RAG/Agent 服务开发。  
> 本笔记在课程基础命令之上，补充了实际服务器使用、常见误区、排障方法和面试关注点。

---

## 目录

1. [学习目标与使用边界](#1-学习目标与使用边界)
2. [Linux、虚拟机与远程连接工具](#2-linux虚拟机与远程连接工具)
3. [目录、路径与文件操作](#3-目录路径与文件操作)
4. [文本查看、查找与管道](#4-文本查看查找与管道)
5. [标准输入、标准输出与重定向](#5-标准输入标准输出与重定向)
6. [Vim、less 与文本阅读](#6-vimless-与文本阅读)
7. [用户、用户组与权限](#7-用户用户组与权限)
8. [进程、后台任务与日志](#8-进程后台任务与日志)
9. [网络、IP、端口与服务](#9-网络ip端口与服务)
10. [环境变量与 Shell 的 `$`](#10-环境变量与-shell-的-)
11. [Python、虚拟环境与 Conda](#11-python虚拟环境与-conda)
12. [软连接、压缩与文件传输](#12-软连接压缩与文件传输)
13. [磁盘与系统状态](#13-磁盘与系统状态)
14. [综合实验：运行并管理 Python HTTP 服务](#14-综合实验运行并管理-python-http-服务)
15. [常见故障排查链路](#15-常见故障排查链路)
16. [面试掌握标准与速查表](#16-面试掌握标准与速查表)

---

# 1. 学习目标与使用边界

对 Python 后端、AI 应用、RAG、Agent 和算法岗位而言，Linux 不需要学到内核或专业运维深度，但应达到：

```text
克隆项目
→ 创建或激活环境
→ 安装依赖
→ 配置环境变量
→ 启动程序
→ 后台运行
→ 查看日志
→ 检查进程和端口
→ 排查错误
→ 安全停止
```

重点不是背下所有参数，而是：

1. 知道某类问题该使用什么工具；
2. 能看懂常见命令；
3. 能独立拼出基础命令；
4. 会使用 `--help`、`man` 和日志继续排查；
5. 明白危险操作的后果。

在共享服务器上，不应随意修改：

- 网卡、IP、默认网关和 DNS；
- SSH 服务配置；
- 防火墙；
- 系统级软件和动态库；
- 其他用户的进程与文件；
- `/etc` 下的重要配置。

---

# 2. Linux、虚拟机与远程连接工具

## 2.1 三个容易混淆的概念

- **Linux**：操作系统。
- **VMware 虚拟机**：一台由软件模拟出来的计算机，可在其中运行 Linux。
- **VSCode Remote SSH**：通过 SSH 连接远程 Linux 的开发工具。

课程环境可能是：

```text
Windows
└── VMware
    └── Linux 虚拟机
```

你的环境可能是：

```text
Windows 上的 VSCode
└── SSH
    └── 远程 Linux 服务器
```

FinalShell、XShell、MobaXterm、PuTTY、Windows Terminal 和 VSCode Remote SSH 的主要区别在于界面、文件传输、调试、插件和会话管理。只要连接的是同一台服务器、同一用户和同一 Shell，Linux 命令语义基本不变。

## 2.2 判断当前终端在哪里

```bash
whoami
hostname
pwd
cat /etc/os-release
echo "$SSH_CONNECTION"
```

典型判断：

```text
PS C:\Users\...        Windows PowerShell
user@server:/data/...  远程 Linux Shell
```

VSCode Remote SSH 编辑远程文件时，保存操作通常直接写入服务器文件系统，使用的 Python、Git、CPU、内存和 GPU 也来自服务器。

---

# 3. 目录、路径与文件操作

## 3.1 Linux 目录结构

Linux 只有一个根目录：

```text
/
```

常见目录：

| 目录 | 作用 |
|---|---|
| `/home` | 普通用户家目录常见位置 |
| `/root` | root 用户家目录 |
| `/etc` | 系统和服务配置 |
| `/var` | 日志、缓存和持续变化的数据 |
| `/tmp` | 临时文件 |
| `/usr` | 大量用户程序与共享资源 |
| `/bin`、`/usr/bin` | 常用命令 |
| `/data` | 非统一标准，服务器中常用于大容量数据 |

家目录由用户账户配置决定，并不要求一定在 `/home/用户名`。

```bash
echo "$HOME"
getent passwd "$(whoami)"
```

## 3.2 绝对路径和相对路径

```text
/data/ljw/project/app.py   绝对路径，从 / 开始
project/app.py             相对路径，从当前目录开始
```

特殊路径：

| 符号 | 含义 |
|---|---|
| `.` | 当前目录 |
| `..` | 上一级目录 |
| `~` | 当前用户家目录 |
| `-` | 对 `cd` 而言，表示上一次目录 |

```bash
cd ~
cd ..
cd -
```

## 3.3 常用文件命令

```bash
pwd                         # 当前目录
ls                          # 列出内容
ls -la                      # 包含隐藏文件，长格式
ls -lh                      # 人类可读大小
mkdir project               # 创建目录
mkdir -p a/b/c              # 连同父目录一起创建
touch file.txt              # 创建空文件或更新时间
cp source.txt target.txt    # 复制文件
cp -r src_dir dst_dir       # 复制目录
mv old.txt new.txt          # 移动或重命名
rm file.txt                 # 删除文件
rm -r directory             # 递归删除目录
```

删除前优先检查：

```bash
pwd
ls -ld 要删除的路径
```

不要把 `rm -rf` 当作普通清理手段。

---

# 4. 文本查看、查找与管道

## 4.1 查看文件

```bash
cat file.txt                # 适合短文件
head -n 20 file.txt         # 前 20 行
tail -n 20 file.txt         # 后 20 行
tail -f app.log             # 持续跟踪新增日志
less file.txt               # 分页阅读长文件
less -N file.txt            # 显示行号
```

## 4.2 `find` 的统一结构

```bash
find 起始路径 查找条件 执行动作
```

例子：

```bash
find . -type f -name "*.py"
```

含义：

```text
从当前目录递归查找
只匹配普通文件
文件名以 .py 结尾
```

常用条件：

| 条件 | 作用 |
|---|---|
| `-type f` | 普通文件 |
| `-type d` | 目录 |
| `-type l` | 符号链接 |
| `-name "*.py"` | 区分大小写的名称匹配 |
| `-iname "*.jpg"` | 忽略大小写 |
| `-maxdepth 2` | 最大搜索深度 |
| `-mindepth 1` | 最小搜索深度 |
| `-size +1G` | 大于 1 GiB |
| `-mtime -7` | 最近若干天内修改 |
| `-mmin -60` | 最近 60 分钟内修改 |
| `-empty` | 空文件或空目录 |

示例：

```bash
find . -maxdepth 2 -type d | sort
```

逐项解释：

```text
find               查找
.                  从当前目录开始
-maxdepth 2        最多进入第二层
-type d            只匹配目录
| sort             把路径交给 sort 排序
```

不显示起始目录 `.`：

```bash
find . -mindepth 1 -maxdepth 2 -type d | sort
```

查找大文件并显示大小：

```bash
find . -type f -size +1G -exec ls -lh {} +
```

对多个扩展名使用逻辑组合：

```bash
find . -type f \( -name "*.py" -o -name "*.sh" \)
```

删除前必须先预览：

```bash
find . -type f -name "*.tmp" -print
# 确认无误后，才考虑：
find . -type f -name "*.tmp" -delete
```

## 4.3 管道符 `|`

统一模型：

```bash
命令1 | 命令2 | 命令3
```

左侧命令的标准输出，成为右侧命令的标准输入。

```bash
find . -type f | sort | head -n 10
```

处理流程：

```text
find 产生路径
→ sort 排序
→ head 保留前 10 行
```

常见组合：

```bash
grep -RIn "error" .
find . -type f -name "*.log" | wc -l
sort items.txt | uniq -c | sort -nr
ps -ef | grep "[p]ython"
```

管道默认只传递标准输出，不自动传递标准错误。

---

# 5. 标准输入、标准输出与重定向

每个进程通常自动拥有三条标准通道：

| 文件描述符 | 名称 | 默认位置 |
|---:|---|---|
| `0` | stdin，标准输入 | 终端键盘 |
| `1` | stdout，标准输出 | 当前终端 |
| `2` | stderr，标准错误 | 当前终端 |

统一模型：

```text
输入文件或键盘
      │ stdin(0)
      ▼
     程序
      ├── stdout(1) → 正常结果
      └── stderr(2) → 错误、警告和诊断
```

## 5.1 常用重定向

```bash
command > out.log                 # stdout 覆盖写入
command >> out.log                # stdout 追加写入
command 2> err.log                # stderr 覆盖写入
command 2>> err.log               # stderr 追加写入
command > out.log 2> err.log      # 分别保存
command > all.log 2>&1            # 合并保存
command >> all.log 2>&1           # 合并追加
command 2>/dev/null               # 丢弃错误
command >/dev/null 2>&1           # 丢弃全部输出
```

`>` 默认等于 `1>`。

## 5.2 `2>&1` 的准确含义

```bash
command > app.log 2>&1
```

Shell 从左到右处理：

1. `> app.log`：让 stdout 指向 `app.log`；
2. `2>&1`：让 stderr 指向 stdout 当前的位置。

最终：

```text
stdout ─┐
        ├── app.log
stderr ─┘
```

`&1` 中的 `&` 表示“文件描述符 1”，不是名为 `1` 的文件。

```bash
2>1
```

会创建一个名为 `1` 的文件，与 `2>&1` 不同。

顺序不同，结果也不同：

```bash
command > app.log 2>&1    # stdout 和 stderr 都进 app.log
command 2>&1 > app.log    # stderr 仍可能留在终端
```

## 5.3 管道与错误输出

```bash
command1 | command2
```

只把 `command1` 的 stdout 送入管道。

把 stdout 和 stderr 都送入管道：

```bash
command1 2>&1 | command2
```

Bash 中还可以：

```bash
command1 |& command2
```

一边显示一边保存：

```bash
python app.py 2>&1 | tee app.log
```

追加保存：

```bash
python app.py 2>&1 | tee -a app.log
```

## 5.4 后台程序常用模板

```bash
nohup python train.py > train.log 2>&1 &
```

含义：

```text
nohup                 忽略终端挂断信号
python train.py        启动程序
> train.log            stdout 写入日志
2>&1                   stderr 合并到同一日志
&                      放到后台
```

查看最近后台进程 PID：

```bash
echo "$!"
```

---

# 6. Vim、less 与文本阅读

## 6.1 Vim 生存技能

Vim 的三类状态：

```text
普通模式 → 编辑、移动、删除、复制
插入模式 → 输入文字
命令行模式 → 保存、退出、跳转
```

常用按键：

| 操作 | 按键 |
|---|---|
| 进入插入模式 | `i` |
| 返回普通模式 | `Esc` |
| 保存 | `:w` |
| 保存并退出 | `:wq` |
| 强制退出不保存 | `:q!` |
| 搜索 | `/关键词` |
| 下一个结果 | `n` |
| 删除当前行 | `dd` |
| 复制当前行 | `yy` |
| 粘贴 | `p` |
| 撤销 | `u` |
| 文件开头 | `gg` |
| 文件结尾 | `G` |

VSCode 是主要编辑器时，Vim 只需达到紧急修改配置和脚本的水平。

## 6.2 `less`

`less` 是分页阅读器，不会默认修改文件。

常用按键：

| 按键 | 作用 |
|---|---|
| `q` | 退出 |
| `Space` | 向下翻页 |
| `b` | 向上翻页 |
| `g` | 开头 |
| `G` | 结尾 |
| `/keyword` | 向下搜索 |
| `n` | 下一个匹配 |
| `N` | 上一个匹配 |

## 6.3 `nl -ba app.py | less`

```bash
nl -ba app.py | less
```

- `nl`：给文本行编号；
- `-b a`：正文所有行都编号，包括空行；
- `-ba` 是 `-b a` 的紧凑写法；
- `| less`：把带行号的结果分页显示。

单纯阅读代码也可以：

```bash
less -N app.py
```

---

# 7. 用户、用户组与权限

## 7.1 用户信息

```bash
whoami
id
groups
getent passwd 用户名
getent group 用户组名
```

注意正确命令是：

```bash
getent passwd
getent group
```

不是 `getenv` 或 `genenv`。

用户名、用户组名和家目录名是三个不同概念。用户的家目录由账户记录指定。

## 7.2 `su` 与 `sudo`

```bash
su - otheruser
```

切换用户并加载目标用户的登录环境。

```bash
sudo command
```

以授权身份执行一条命令。是否可用取决于系统管理员配置。

共享服务器上不要因为命令失败就盲目加 `sudo`。

## 7.3 权限模型

```text
-rwxr-xr--
│││ │││ │││
│││ │││ └── 其他用户
│││ └────── 用户组
│└───────── 文件所有者
└────────── 文件类型
```

权限数值：

| 数值 | 权限 |
|---:|---|
| `4` | 读 `r` |
| `2` | 写 `w` |
| `1` | 执行 `x` |

```bash
chmod +x manage.sh
chmod 755 manage.sh
chmod 644 config.yml
```

不要把 `chmod 777` 当作通用解决方案。

修改所有者：

```bash
chown user:group file
```

通常需要管理员权限。

目录权限中的 `x` 代表可以进入或穿过目录，而不只是“执行文件”。

---

# 8. 进程、后台任务与日志

## 8.1 查看进程

```bash
ps -ef
ps aux
ps -fp PID
pgrep -af "python app.py"
top
```

避免让 `grep` 匹配自己：

```bash
ps -ef | grep "[p]ython"
```

查看进程更底层的信息：

```bash
readlink -f /proc/PID/exe
readlink -f /proc/PID/cwd
tr '\0' ' ' < /proc/PID/cmdline
echo
```

## 8.2 信号与停止程序

```bash
kill PID        # 默认发送 SIGTERM，允许程序清理
kill -9 PID     # SIGKILL，立即终止，最后手段
```

前台程序中：

```text
Ctrl+C → 发送 SIGINT
```

先确认 PID 和程序归属，再停止。不要终止其他用户的任务。

## 8.3 前台、后台、`nohup` 与 `tmux`

```bash
command &       # 当前 Shell 后台运行
jobs -l         # 查看当前 Shell 作业
fg %1           # 拉回前台
```

`&` 本身不保证 SSH 断开后继续运行。常见方式：

```bash
nohup command > app.log 2>&1 &
```

复杂训练和交互式任务更适合 `tmux`，因为它保存完整终端会话。

日志查看：

```bash
tail -n 100 app.log
tail -f app.log
grep -n "Traceback" app.log
grep -i "error" app.log
```

---

# 9. 网络、IP、端口与服务

## 9.1 基本概念

```text
IP 地址：标识网络中的主机或接口
端口：标识主机上的具体网络进程
协议：规定通信规则，如 TCP、UDP、HTTP
Socket：IP、端口、协议等共同构成的通信端点
```

一次连接可以表示为：

```text
客户端IP:临时端口  →  服务器IP:服务端口
```

例如：

```text
192.168.1.50:53124 → 192.168.1.20:22
```

## 9.2 特殊地址

- `127.0.0.1`：IPv4 回环地址，只在本机内部通信。
- `0.0.0.0`：在服务绑定时通常表示所有本机 IPv4 接口；它不是普通客户端应连接的目标地址。
- 服务器真实 IP：对应某块网卡，可用于局域网或外部访问，仍受路由和防火墙限制。

```bash
ip -br addr
ip route
hostname -I
```

现代 Linux 通常优先使用 `ip`，而不是旧式 `ifconfig`。

## 9.3 TCP 与 UDP

TCP：

- 面向连接；
- 可靠、有序；
- 有 `LISTEN`、`ESTABLISHED`、`TIME_WAIT` 等状态；
- 常用于 SSH、HTTP、数据库。

UDP：

- 无 TCP 式连接建立过程；
- 不保证可靠、有序；
- 开销较小；
- 常用于 DNS、实时音视频和部分监控协议。

## 9.4 查看端口：`ss`、`netstat` 与 `nmap`

本机查看监听套接字：

```bash
ss -lntp        # TCP
ss -lunp        # UDP
ss -lntup       # TCP + UDP
```

查看所有 TCP 连接：

```bash
ss -ant
```

常见地址：

```text
127.0.0.1:8000   只接受本机访问
0.0.0.0:8000     监听所有 IPv4 接口
```

`netstat` 是较老工具，常见对应关系：

```bash
netstat -lntup
netstat -ant
```

`ss` 通常更适合现代 Linux。

`nmap` 是从扫描位置探测目标主机端口的工具；它回答的是“从这里看，目标端口能否访问”，并不等同于目标机内部的监听状态。

```bash
nmap 目标地址
nmap -p 22,80,443 目标地址
nmap -p- 目标地址
```

仅扫描自己拥有或明确获授权的系统。

## 9.5 常见 TCP 状态

| 状态 | 含义 |
|---|---|
| `LISTEN` | 服务端等待新连接 |
| `ESTABLISHED` | 连接已建立 |
| `SYN_SENT` | 主动发起连接，等待响应 |
| `SYN_RECV` | 收到连接请求，握手未完成 |
| `TIME_WAIT` | 主动关闭后短暂保留记录 |
| `CLOSE_WAIT` | 对方已关闭，本地应用尚未关闭 |
| `FIN_WAIT1/2` | 主动关闭过程中的中间状态 |

## 9.6 `ping`、`curl` 与 DNS

```bash
ping -c 4 127.0.0.1
curl -v http://127.0.0.1:18080/health
getent hosts example.com
```

- `ping` 主要测试 ICMP 可达性；
- `curl` 测试应用层请求；
- `getent hosts` 查看系统解析域名的结果。

`ping` 不通不一定意味着 HTTP 或 SSH 不通，因为 ICMP 可能被禁用。

---

# 10. 环境变量与 Shell 的 `$`

## 10.1 环境变量是什么

环境变量是一组传给进程的键值配置：

```text
PATH=/usr/local/bin:/usr/bin:/bin
HOME=/home/user
CUDA_VISIBLE_DEVICES=0
```

Shell 普通变量：

```bash
NAME="linux"
```

导出给子进程：

```bash
export NAME="linux"
```

读取：

```bash
echo "$NAME"
```

取消：

```bash
unset NAME
```

## 10.2 `$` 的常见用法

| 形式 | 含义 |
|---|---|
| `$VAR` | 读取变量 |
| `${VAR}` | 明确变量边界 |
| `${VAR:-default}` | 未设置或为空时使用默认值 |
| `$(command)` | 执行命令并取得输出 |
| `$((a + b))` | 算术展开 |
| `$?` | 上一条命令退出状态 |
| `$!` | 最近后台进程 PID |
| `$$` | 当前 Shell PID |
| `$0` | 脚本名 |
| `$1`、`$2` | 脚本参数 |
| `$#` | 参数个数 |
| `"$@"` | 保留边界的全部参数 |

赋值时不加 `$`：

```bash
NAME="linux"
```

取值时加 `$`：

```bash
echo "$NAME"
```

变量引用默认使用双引号：

```bash
cd "$PROJECT_ROOT"
```

单引号不展开变量：

```bash
echo '$HOME'   # 原样输出 $HOME
```

双引号会展开：

```bash
echo "$HOME"
```

## 10.3 `PATH`

`PATH` 决定 Shell 去哪些目录寻找命令：

```bash
echo "$PATH"
command -v python
type -a python
```

临时添加目录：

```bash
export PATH="/data/ljw/tools/bin:$PATH"
```

不要写成：

```bash
export PATH="/data/ljw/tools/bin"
```

否则原有搜索路径会被覆盖。

## 10.4 作用范围

只对一条命令：

```bash
CUDA_VISIBLE_DEVICES=2 python train.py
```

当前终端会话：

```bash
export CUDA_VISIBLE_DEVICES=2
```

每次打开 Bash 自动设置：写入 `~/.bashrc`，然后：

```bash
source ~/.bashrc
```

临时实验变量不应随意永久写入 `.bashrc`。

---

# 11. Python、虚拟环境与 Conda

## 11.1 `python` 与 `python3`

`python3` 明确要求 Python 3，但不固定具体小版本。

```bash
python3 --version
```

`python` 的含义取决于系统或当前虚拟环境，可能：

- 指向 Python 3；
- 在老系统中指向 Python 2；
- 根本不存在。

检查：

```bash
command -v python
command -v python3
python --version
python3 --version
python -c 'import sys; print(sys.executable)'
python3 -c 'import sys; print(sys.executable)'
```

在已激活的 Conda 或 `venv` 环境中，一般优先使用：

```bash
python
python -m pip
```

未激活环境时，Linux 上常用：

```bash
python3
python3 -m pip
```

## 11.2 `python3 -m py_compile app.py`

```bash
python3 -m py_compile app.py
```

拆解：

```text
python3       启动 Python 3 解释器
-m            把后面的名称作为模块运行
py_compile    标准库编译模块
app.py        待编译的源码
```

它会解析并编译源码，因此可发现：

- 括号或引号未闭合；
- 漏写冒号；
- 非法缩进；
- 其他语法错误。

成功时通常无输出：

```bash
python3 -m py_compile app.py
echo "$?"
```

`0` 通常表示成功。

它不能发现运行时或逻辑错误，例如除零、文件不存在、网络错误和算法结果错误。

检查整个目录：

```bash
python3 -m compileall -q .
```

## 11.3 `-m` 的价值

```bash
python -m pip install requests
python -m venv .venv
python -m http.server 8000
python -m pytest
```

`python -m ...` 能确保运行的模块属于前面这套 Python 环境，避免 `pip` 与 `python` 指向不同环境。

## 11.4 虚拟环境与环境变量的区别

环境变量：

```text
程序运行时读取的配置键值
```

虚拟环境：

```text
相互隔离的 Python 解释器、命令和依赖集合
```

虚拟环境不是环境变量，但激活环境通常会修改 `PATH` 等环境变量。

## 11.5 Conda 的定位

Conda 同时是：

1. 环境管理器；
2. 包和依赖管理器。

常用命令：

```bash
conda info --envs
conda env list
conda create -n rag-dev python=3.11
conda activate rag-dev
conda deactivate
conda list
conda install numpy
conda remove numpy
conda env remove -n rag-dev
conda create -n backup-env --clone old-env
conda run -n rag-dev python --version
```

当前环境变量：

```bash
echo "${CONDA_DEFAULT_ENV:-未激活}"
echo "${CONDA_PREFIX:-未激活}"
echo "${CONDA_SHLVL:-0}"
```

- `CONDA_DEFAULT_ENV`：当前环境名称；
- `CONDA_PREFIX`：当前环境路径；
- `CONDA_SHLVL`：激活层级。

更完整地确认：

```bash
conda info --envs
python -c 'import sys; print(sys.executable)'
python -m pip --version
```

导出环境：

```bash
conda env export --from-history > environment.yml
```

创建环境：

```bash
conda env create -f environment.yml
```

避免把所有项目依赖都装进 `base`。大型深度学习环境中不要随意执行全量更新。

---

# 12. 软连接、压缩与文件传输

## 12.1 软连接

软连接类似快捷方式：

```bash
ln -s 目标路径 链接名称
```

顺序是：

```text
先目标，后链接
```

例子：

```bash
ln -s /data/datasets/VisDrone ./data/visdrone
```

查看：

```bash
ls -l ./data/visdrone
readlink ./data/visdrone
readlink -f ./data/visdrone
```

删除软连接：

```bash
rm ./data/visdrone
```

通常只删除链接，不删除目标。

目标删除后，软连接可能成为失效链接：

```bash
find . -xtype l
```

更新链接前先确认对象类型：

```bash
ls -ld link_name
ln -sfn 新目标 link_name
```

## 12.2 软连接与硬链接

| 特征 | 软连接 | 硬链接 |
|---|---|---|
| 命令 | `ln -s` | `ln` |
| 保存内容 | 目标路径 | 指向同一 inode |
| 跨文件系统 | 可以 | 不可以 |
| 目标名删除后 | 可能失效 | 内容仍存在 |
| 目录链接 | 常用 | 普通用户通常受限制 |

AI 项目中软连接常用于共享数据集、模型权重和当前版本路径。

## 12.3 `tar`

压缩：

```bash
tar -czvf project.tar.gz project/
```

解压：

```bash
tar -xzvf project.tar.gz
```

解压到指定目录：

```bash
tar -xzvf project.tar.gz -C target_dir
```

查看归档内容：

```bash
tar -tzf project.tar.gz
```

常用参数：

```text
-c 创建
-x 解包
-t 查看
-z gzip
-v 显示过程
-f 指定归档文件
-C 指定目标目录
```

## 12.4 `scp`

从本地上传：

```bash
scp local.txt user@server:/remote/path/
```

从服务器下载：

```bash
scp user@server:/remote/path/file.txt .
```

递归传目录：

```bash
scp -r local_dir user@server:/remote/path/
```

SSH 自定义端口：

```bash
ssh -p 2222 user@server
scp -P 2222 file user@server:/path/
```

`ssh` 使用小写 `-p`，`scp` 使用大写 `-P`。

大规模增量同步通常更适合 `rsync`。

---

# 13. 磁盘与系统状态

## 13.1 磁盘空间

查看文件系统：

```bash
df -h
df -h /data
```

查看目录大小：

```bash
du -sh .
du -h --max-depth=1 | sort -h
```

查找大文件：

```bash
find . -type f -size +1G -exec ls -lh {} +
```

`df` 查看文件系统整体空间；`du` 统计文件和目录实际占用。

## 13.2 系统状态

```bash
top
free -h
uptime
```

安装了相关工具时：

```bash
iostat
sar -n DEV 1
```

不要只看一个瞬时值，要关注持续趋势和程序行为。

---

# 14. 综合实验：运行并管理 Python HTTP 服务

## 14.1 实验目标

理解以下链路：

```text
Python 源文件
→ Python 解释器
→ Linux 进程
→ 创建 TCP socket
→ 监听 127.0.0.1:18080
→ curl 发送 HTTP 请求
→ 服务返回 JSON
→ stdout/stderr 写日志
→ 信号停止进程
```

## 14.2 语法检查

```bash
python3 -m py_compile app.py
echo "$?"
```

## 14.3 前台启动

```bash
python3 app.py
```

示例输出：

```text
[startup] app_name=linux-capstone app_env=development host=127.0.0.1 port=18080
[warning] 当前运行在 development 环境
[ready] 服务地址：http://127.0.0.1:18080
```

这不只是“运行 Python 文件”，而是：

1. 读取默认配置、环境变量和命令行参数；
2. 创建一个 Linux 进程；
3. 绑定 IP 与端口；
4. 进入持续等待请求的状态；
5. 分别向 stdout 和 stderr 输出日志。

终端没有返回命令提示符，通常是因为服务在前台持续运行，不是卡死。

## 14.4 另一个终端验证

```bash
curl -i http://127.0.0.1:18080/health
ss -lntp | grep ':18080'
pgrep -af "python3 app.py"
```

`curl` 验证应用层服务，`ss` 验证内核监听状态，`pgrep` 验证进程。

## 14.5 环境变量启动

```bash
APP_NAME="topo-service" \
APP_ENV="testing" \
APP_PORT="18081" \
python3 app.py
```

这些变量只对本次命令有效。

## 14.6 后台启动

```bash
APP_ENV=production \
nohup python3 app.py \
--host 127.0.0.1 \
--port 18080 \
> logs/app.log 2>&1 &
```

保存 PID：

```bash
echo "$!" > run/app.pid
```

检查：

```bash
ps -fp "$(cat run/app.pid)"
ss -lntp | grep ':18080'
tail -f logs/app.log
```

停止：

```bash
PID="$(cat run/app.pid)"
ps -fp "$PID"
kill "$PID"
```

确认后删除 PID 文件：

```bash
rm -f run/app.pid
```

## 14.7 端口冲突实验

已有服务监听 `18080` 时，再启动一个实例：

```bash
python3 app.py --port 18080
```

可能出现：

```text
Address already in use
```

排查：

```bash
ss -lntp | grep ':18080'
ps -fp PID
```

正确处理顺序：

```text
确认占用端口的程序
→ 判断是否属于自己
→ 正常停止旧程序或更换端口
```

---

# 15. 常见故障排查链路

## 15.1 `command not found`

```bash
command -v python
type -a python
echo "$PATH"
conda info --envs
```

可能原因：

- 程序未安装；
- 虚拟环境未激活；
- `PATH` 中没有程序目录；
- 命令名称不同，如只有 `python3`。

## 15.2 `Permission denied`

```bash
ls -l file
ls -ld directory
id
```

可能原因：

- 文件没有读或执行权限；
- 目录没有 `x` 权限；
- 所有者或用户组不匹配；
- 共享目录权限限制。

自己的脚本：

```bash
chmod +x run.sh
```

不要直接使用 `chmod 777`。

## 15.3 端口被占用

```bash
ss -lntp | grep ':8000'
ps -fp PID
```

确认后：

```bash
kill PID
```

## 15.4 服务启动了但访问不了

```text
1. 进程是否存在
2. 端口是否监听
3. 监听地址是 127.0.0.1、具体 IP 还是 0.0.0.0
4. 服务器本机 curl 是否成功
5. 目标 IP、DNS 和路由是否正确
6. 防火墙或访问控制是否阻止
7. 日志中是否有异常
```

命令：

```bash
pgrep -af "app"
ss -lntp
curl -v http://127.0.0.1:8000/health
ip -br addr
ip route
getent hosts 域名
tail -n 100 app.log
```

常见错误：

- `Connection refused`：目标可达，但没有程序接受连接，或被明确拒绝；
- `Connection timed out`：网络路径、防火墙或服务响应可能存在问题；
- `404`：服务可访问，但路径不存在；
- `500`：请求到达服务，但服务内部执行失败。

## 15.5 磁盘满

```bash
df -h
du -h --max-depth=1 | sort -h
find . -type f -size +1G -exec ls -lh {} +
```

## 15.6 Python 环境混乱

```bash
echo "${CONDA_DEFAULT_ENV:-未激活}"
echo "${CONDA_PREFIX:-未激活}"
python -c 'import sys; print(sys.executable)'
python -m pip --version
python -c 'import 包名; print(包名.__file__)'
```

---

# 16. 面试掌握标准与速查表

## 16.1 AI/Python 岗位常见 Linux 问法

应能解释并操作：

- 如何查看当前目录和文件；
- 如何查找文件或日志关键字；
- 如何修改脚本执行权限；
- SSH 断开后如何保持训练运行；
- 如何查看训练日志；
- 如何找到某个 Python 进程；
- 如何排查端口占用；
- `127.0.0.1` 与 `0.0.0.0` 的区别；
- `>`、`>>`、`2>`、`2>&1` 的区别；
- `PATH`、环境变量和虚拟环境的关系；
- `python`、`python3`、`python -m pip` 的区别；
- Conda 激活后发生了什么；
- 磁盘满、权限不足、命令找不到如何排查。

## 16.2 必须熟练的命令

```bash
pwd
ls -la
cd
mkdir -p
cp
mv
rm
cat
less
head
tail -f
grep
find
sort
wc
chmod
id
ps
pgrep
top
kill
jobs
nohup
ip
ping
curl
ssh
scp
ss
df
du
tar
env
export
source
command -v
python -m pip
conda info --envs
```

## 16.3 高频模板

```bash
# 查找 Python 文件
find . -type f -name "*.py"

# 查找错误日志
grep -RIn "error" .

# 查看日志
tail -f train.log

# 后台训练
nohup python train.py > train.log 2>&1 &

# 查看后台 PID
echo "$!"

# 查进程
pgrep -af "python train.py"

# 查端口
ss -lntp | grep ':8000'

# 测试服务
curl -v http://127.0.0.1:8000/health

# 查看磁盘
df -h
du -h --max-depth=1 | sort -h

# 检查 Python 环境
echo "${CONDA_DEFAULT_ENV:-未激活}"
python -c 'import sys; print(sys.executable)'
python -m pip --version

# 语法检查
python -m py_compile app.py

# 打包项目
tar -czvf project.tar.gz project/
```

## 16.4 最终判断

达到以下能力，就可以停止单独刷 Linux 课程，在 Git、Python 工程化、FastAPI、Docker、RAG 和 Agent 项目中继续巩固：

```text
能创建和管理文件
能搜索和阅读日志
能理解权限
能运行和停止进程
能后台启动任务
能检查端口和服务
能配置环境变量
能确认 Python/Conda 环境
能定位常见报错
能安全打包和传输文件
```

---

## 参考学习方式

不要尝试一次记住所有选项。更有效的方法是：

```text
课程建立概念
→ 小实验形成操作记忆
→ 项目中反复使用
→ 遇到复杂参数再查手册
```

常用帮助：

```bash
command --help
man command
```

GitHub 仓库中建议同时保留：

```text
README.md               项目说明和实验入口
Linux_Study_Notes.md    系统笔记
scripts/                练习脚本
logs/                   不提交实际大日志
.gitignore              排除缓存、环境和日志
```

建议 `.gitignore`：

```gitignore
__pycache__/
*.pyc
*.log
*.pid
.venv/
.env
.DS_Store
```
