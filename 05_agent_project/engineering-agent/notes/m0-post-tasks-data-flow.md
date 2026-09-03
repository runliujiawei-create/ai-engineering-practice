# M0 学习笔记：POST /tasks 真实请求数据流

本文档总结目前已经学过的 M0 代码层知识点，重点是：

- HTTP 请求是什么
- FastAPI 如何把请求交给函数
- Router 是什么
- Pydantic Schema 如何校验请求体
- `TaskCreate`、`TaskRead` 的职责
- `memory.create_task(...)` 如何真正创建并保存 Task
- `main.py`、`tasks.py`、`task.py`、`memory.py` 之间的逻辑关系

当前阶段只关注：

```text
POST /tasks
```

暂时不深入 Agent Loop、LLM、Tool Calling、MCP、RAG、PostgreSQL、Redis、Sandbox、Human Approval、Evaluation。

---

## 1. HTTP 请求基础

一个 HTTP 请求可以理解为客户端发给后端的一封标准格式的消息。

常见组成：

```text
HTTP Method
URL / Path
Headers
Body
```

例如创建 Task 的请求：

```http
POST /tasks
Content-Type: application/json

{
  "goal": "Build an agent backend"
}
```

含义：

```text
POST
表示这次请求通常用于创建资源或触发动作。

/tasks
表示这次请求访问 tasks 这个资源集合。

Content-Type: application/json
表示请求体 Body 使用 JSON 格式。

{"goal": "Build an agent backend"}
表示客户端提交给后端的具体数据。
```

### GET 和 POST 的区别

`GET` 通常用于读取数据。

例如：

```http
GET /tasks/task_001
```

意思是读取 ID 为 `task_001` 的 Task。

`POST` 通常用于创建数据或触发动作。

例如：

```http
POST /tasks
```

意思是创建一个新的 Task。

再例如：

```http
POST /tasks/task_001/runs
```

意思是给 ID 为 `task_001` 的 Task 创建一次 Run。

### URL Path 和路径参数

FastAPI 中写：

```python
@router.get("/tasks/{task_id}")
```

这里的 `{task_id}` 是路径参数，不是固定字符串。

如果请求是：

```http
GET /tasks/task_001
```

FastAPI 会得到：

```python
task_id = "task_001"
```

### 请求体 Body

请求体用于携带客户端提交给服务器的主要数据。

创建 Task 时，只写：

```http
POST /tasks
```

还不够，因为服务器不知道你要创建什么 Task。

所以需要请求体：

```json
{
  "goal": "Build an agent backend"
}
```

这个 body 的意思是：

```text
我要创建的 Task 的目标是 Build an agent backend。
```

### JSON 是什么

JSON 是一种数据格式，不是 Python 专属的数据类型。

JSON 常用于客户端和后端之间传输数据。

常见 JSON 值类型：

```text
string
number
boolean
array
object
null
```

例子：

```json
{
  "goal": "Build an agent backend",
  "priority": 1,
  "urgent": false,
  "tags": ["agent", "backend"],
  "metadata": {
    "source": "learning"
  },
  "deadline": null
}
```

对应到 Python 里大概会变成：

```python
{
    "goal": "Build an agent backend",
    "priority": 1,
    "urgent": False,
    "tags": ["agent", "backend"],
    "metadata": {"source": "learning"},
    "deadline": None,
}
```

---

## 2. 项目文件职责

当前 M0 后端项目的核心结构：

```text
engineering-agent/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── tasks.py
│   │   └── runs.py
│   ├── schemas/
│   │   ├── task.py
│   │   ├── run.py
│   │   └── event.py
│   ├── services/
│   │   └── run_service.py
│   └── storage/
│       └── memory.py
├── tests/
│   ├── conftest.py
│   ├── test_tasks.py
│   └── test_runs.py
├── pyproject.toml
├── README.md
└── .gitignore
```

核心职责：

```text
app/main.py
创建 FastAPI 应用，并把各个 router 注册进 app。

app/api/tasks.py
定义 Task 相关 HTTP 接口，比如 POST /tasks。

app/schemas/task.py
定义 Task 的请求和响应数据结构，比如 TaskCreate、TaskRead。

app/storage/memory.py
使用 Python 内存保存 Task、Run、Event。

app/services/run_service.py
负责 Run 创建相关流程，后续学习 POST /tasks/{task_id}/runs 时再重点看。
```

---

## 3. main.py：应用入口

真实代码：

```python
from fastapi import FastAPI

from app.api import runs, tasks


app = FastAPI(title="engineering-agent")

app.include_router(tasks.router)
app.include_router(runs.router)
```

重点概念：

```python
app = FastAPI(title="engineering-agent")
```

创建 FastAPI 应用对象。

`title="engineering-agent"` 是传给 FastAPI 的配置，通常会显示在 `/docs` 文档页面中。

```python
app.include_router(tasks.router)
```

把 `tasks.py` 里定义的路由注册到 FastAPI 应用上。

如果没有这一行，即使 `tasks.py` 里写了 `@router.post("/tasks")`，主应用也不知道这个接口存在。

逻辑关系：

```text
main.py 创建总 app
tasks.py 创建 tasks.router
main.py 通过 include_router 把 tasks.router 加入 app
FastAPI app 才能接收 POST /tasks
```

---

## 4. Router 是什么

Router 可以理解为一张请求分发表。

它记录：

```text
HTTP 方法 + URL Path -> Python 函数
```

例如：

```text
POST /tasks -> create_task(...)
GET /tasks/{task_id} -> get_task(...)
POST /tasks/{task_id}/runs -> create_run(...)
```

在 `tasks.py` 里：

```python
router = APIRouter()
```

创建一个 router。

后面通过：

```python
@router.post("/tasks")
```

把某个函数登记到这个 router 里。

---

## 5. tasks.py：HTTP 接口层

与 `POST /tasks` 相关的核心代码：

```python
@router.post("/tasks", response_model=TaskRead)
def create_task(payload: TaskCreate) -> TaskRead:
    return memory.create_task(goal=payload.goal)
```

### `@` 是什么

`@router.post(...)` 是 Python 装饰器语法。

在 FastAPI 里，装饰器用于把下面的普通 Python 函数注册成 HTTP 接口。

```python
@router.post("/tasks")
def create_task(...):
    ...
```

意思是：

```text
以后收到 POST /tasks 请求时，调用下面这个 create_task 函数。
```

装饰器作用于它紧跟着的函数。

### `@router.post("/tasks", response_model=TaskRead)`

参数含义：

```text
router
当前文件里创建的 APIRouter 对象。

.post(...)
表示这个接口处理 HTTP POST 请求。

"/tasks"
表示 URL path。

response_model=TaskRead
表示响应数据要按照 TaskRead 这个 schema 输出。
```

### `def create_task(payload: TaskCreate) -> TaskRead`

这是 Python 函数定义。

参数含义：

```text
def
定义函数。

create_task
函数名。

payload
函数参数名，表示请求体解析后的对象。

payload: TaskCreate
类型标注。FastAPI 会根据这个标注，把 JSON body 解析并校验成 TaskCreate 对象。

-> TaskRead
返回类型标注，表示这个函数预计返回 TaskRead。
```

注意：

```text
真正让响应按 TaskRead 输出的是 response_model=TaskRead。
-> TaskRead 更多是给人、编辑器、类型检查工具看的。
```

### `return memory.create_task(goal=payload.goal)`

这一行是真正调用存储层创建 Task 的地方。

拆开：

```text
payload.goal
从请求体对象里取出 goal 字段。

memory.create_task(...)
调用 memory.py 里的 create_task 方法。

goal=payload.goal
把请求体里的 goal 作为参数传给存储层。

return
把 memory 创建好的 Task 返回给 FastAPI。
```

---

## 6. FastAPI 为什么会校验请求体

关键代码：

```python
def create_task(payload: TaskCreate) -> TaskRead:
```

FastAPI 会观察函数签名。

它看到：

```python
payload: TaskCreate
```

并发现 `TaskCreate` 继承自 Pydantic 的 `BaseModel`。

于是 FastAPI 推断：

```text
payload 应该来自 HTTP 请求体 body。
body 应该用 TaskCreate 解析和校验。
```

内部过程可以近似理解为：

```python
body = {"goal": "Build an agent backend"}
payload = TaskCreate(**body)
create_task(payload)
```

如果校验失败，FastAPI 不会进入 `create_task` 函数，而是直接返回错误，通常是 `422 Unprocessable Entity`。

---

## 7. task.py：Pydantic Schema

真实代码：

```python
from typing import Literal

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    goal: str = Field(min_length=1)


class TaskRead(BaseModel):
    id: str
    goal: str
    status: Literal["pending"]
```

### `BaseModel`

`BaseModel` 是 Pydantic 提供的基础类。

继承它以后：

```python
class TaskCreate(BaseModel):
    goal: str
```

Pydantic 会自动提供：

```text
对象创建能力
字段类型校验能力
错误信息生成能力
JSON 转换能力
字段访问能力
```

不用手写：

```python
def __init__(self, goal):
    self.goal = goal
```

### `TaskCreate`

```python
class TaskCreate(BaseModel):
    goal: str = Field(min_length=1)
```

含义：

```text
创建 Task 时，客户端必须传 goal。
goal 必须是字符串。
goal 长度至少为 1，不能为空字符串。
```

合法请求：

```json
{
  "goal": "Build an agent backend"
}
```

不合法请求：

```json
{
  "goal": ""
}
```

也不符合当前代码预期：

```json
{
  "title": "Build an agent backend",
  "description": "Create the M0 skeleton"
}
```

因为当前 `TaskCreate` 只定义了 `goal` 字段。

### `Field`

`Field` 是 Pydantic 提供的字段配置函数。

常见用法：

```python
name: str = Field(min_length=2, max_length=20)
age: int = Field(ge=0)
score: float = Field(gt=0, le=100)
```

在当前项目里：

```python
goal: str = Field(min_length=1)
```

表示：

```text
goal 是字符串，并且最短长度为 1。
```

### `TaskRead`

```python
class TaskRead(BaseModel):
    id: str
    goal: str
    status: Literal["pending"]
```

表示返回给客户端的 Task 数据结构。

字段：

```text
id
Task 的唯一 ID，字符串。

goal
Task 的目标，字符串。

status
Task 当前状态，目前只能是 "pending"。
```

示例响应：

```json
{
  "id": "task_001",
  "goal": "Build an agent backend",
  "status": "pending"
}
```

### 为什么分 TaskCreate 和 TaskRead

因为请求输入和响应输出不是同一件事。

创建 Task 时，客户端只需要提交：

```json
{
  "goal": "Build an agent backend"
}
```

服务器返回时，需要包含：

```json
{
  "id": "task_001",
  "goal": "Build an agent backend",
  "status": "pending"
}
```

所以：

```text
TaskCreate
定义客户端创建 Task 时可以提交什么。

TaskRead
定义客户端读取或创建成功后能看到什么。
```

客户端不应该自己决定 `id` 和初始 `status`，这些应该由后端生成。

---

## 8. memory.py：内存存储层

与 `POST /tasks` 相关的核心代码：

```python
class MemoryStorage:
    def __init__(self) -> None:
        self.tasks: dict[str, TaskRead] = {}
        self.runs: dict[str, RunRead] = {}
        self.events: dict[str, list[EventRead]] = {}
        self._task_count = 0
        self._run_count = 0
        self._event_count = 0

    def create_task(self, goal: str) -> TaskRead:
        self._task_count += 1
        task = TaskRead(
            id=f"task_{self._task_count:03d}",
            goal=goal,
            status="pending",
        )
        self.tasks[task.id] = task
        return task


memory = MemoryStorage()
```

### `MemoryStorage`

`MemoryStorage` 是一个类。

它负责在 Python 内存里保存：

```text
tasks
runs
events
```

它不是 HTTP 层，不关心 URL、Header、Body。

### `__init__`

```python
def __init__(self) -> None:
```

`__init__` 是 Python 类的初始化方法。

创建对象时会自动执行：

```python
memory = MemoryStorage()
```

### `self`

`self` 表示当前对象自己。

如果：

```python
memory = MemoryStorage()
```

那么在这个对象的方法里，`self` 就代表这个 `memory` 对象。

### `self.tasks`

```python
self.tasks: dict[str, TaskRead] = {}
```

含义：

```text
self.tasks 是一个字典。
key 是 task_id，类型是 str。
value 是 TaskRead 对象。
```

示例：

```python
{
    "task_001": TaskRead(
        id="task_001",
        goal="Build an agent backend",
        status="pending",
    )
}
```

使用 dict 的原因：

```text
可以通过 task_id 快速查询 Task。
```

### 计数器

```python
self._task_count = 0
```

用于生成简单 ID。

变量名前面的 `_` 是 Python 命名习惯，表示这个属性主要给类内部使用。

### `create_task`

```python
def create_task(self, goal: str) -> TaskRead:
```

含义：

```text
创建一个新的 Task。
参数 goal 是字符串。
返回 TaskRead 对象。
```

```python
self._task_count += 1
```

计数器加一。

等价于：

```python
self._task_count = self._task_count + 1
```

```python
task = TaskRead(
    id=f"task_{self._task_count:03d}",
    goal=goal,
    status="pending",
)
```

创建一个 `TaskRead` 对象。

`f"task_{self._task_count:03d}"` 是 f-string。

`:03d` 表示：

```text
把整数格式化为至少 3 位，不够前面补 0。
```

示例：

```text
1 -> 001
2 -> 002
12 -> 012
123 -> 123
```

所以生成：

```text
task_001
task_002
task_003
```

```python
self.tasks[task.id] = task
```

真正保存 Task 的地方。

如果：

```python
task.id = "task_001"
```

那么这行等价于：

```python
self.tasks["task_001"] = task
```

```python
return task
```

把创建好的 Task 返回给调用方。

### `memory = MemoryStorage()`

```python
memory = MemoryStorage()
```

创建一个全局共享的内存存储对象。

`tasks.py` 里通过：

```python
from app.storage.memory import memory
```

导入并使用这个对象。

这样多个请求访问的是同一个 `memory` 对象。

如果每次请求都重新创建 `MemoryStorage()`，之前保存的 Task 就可能查不到。

---

## 9. POST /tasks 完整流程

以这个请求为例：

```http
POST /tasks
Content-Type: application/json

{
  "goal": "Build an agent backend"
}
```

完整数据流：

```text
1. 客户端发送 HTTP 请求
   POST /tasks
   Body 是 JSON：{"goal": "Build an agent backend"}

2. FastAPI app 接收请求
   app/main.py 里创建了 app。

3. app 找到 tasks router
   因为 main.py 里执行了：
   app.include_router(tasks.router)

4. tasks router 匹配路由
   找到：
   @router.post("/tasks", response_model=TaskRead)

5. FastAPI 准备调用 create_task 函数
   函数签名是：
   def create_task(payload: TaskCreate) -> TaskRead

6. FastAPI 解析请求体
   读取 JSON body。

7. Pydantic 校验请求体
   使用 TaskCreate：
   goal 必须存在。
   goal 必须是 str。
   goal 长度至少为 1。

8. FastAPI 创建 payload 对象
   payload.goal = "Build an agent backend"

9. 进入 create_task 函数
   执行：
   memory.create_task(goal=payload.goal)

10. memory.py 创建 Task
    _task_count 加一。
    创建 TaskRead：
    id="task_001"
    goal="Build an agent backend"
    status="pending"

11. memory.py 保存 Task
    self.tasks["task_001"] = task

12. memory.py 返回 task
    返回给 tasks.py 的 create_task。

13. tasks.py 返回 task
    返回给 FastAPI。

14. FastAPI 整理响应
    根据 response_model=TaskRead 输出 JSON。

15. 客户端收到响应
```

示例响应：

```json
{
  "id": "task_001",
  "goal": "Build an agent backend",
  "status": "pending"
}
```

---

## 10. 最重要的记忆点

```text
main.py
负责创建 FastAPI app，并注册 router。

tasks.py
负责定义 HTTP 接口，把请求交给 Python 函数处理。

task.py
负责定义请求和响应的数据结构。

memory.py
负责真正创建、保存、查询内存数据。
```

```text
@router.post("/tasks")
把 POST /tasks 请求绑定到下面的 create_task 函数。
```

```text
payload: TaskCreate
告诉 FastAPI：请求体要用 TaskCreate 解析和校验。
```

```text
response_model=TaskRead
告诉 FastAPI：响应体要按 TaskRead 输出。
```

```text
Field(min_length=1)
给 goal 字段增加校验规则：字符串长度至少为 1。
```

```text
memory.create_task(goal=payload.goal)
把请求里的 goal 交给存储层，真正创建并保存 Task。
```

```text
self.tasks[task.id] = task
把 TaskRead 对象保存到内存字典里。
```

---

## 11. 自测问题

1. `POST /tasks` 是读取 Task，还是创建 Task？
2. `GET /tasks/{task_id}` 里的 `{task_id}` 是什么意思？
3. 请求体 Body 的作用是什么？
4. JSON 是 Python 数据类型，还是跨系统传输的数据格式？
5. `@router.post("/tasks")` 绑定的是哪个函数？
6. `payload: TaskCreate` 为什么能触发请求体校验？
7. `TaskCreate` 和 `TaskRead` 为什么要分开？
8. `Field(min_length=1)` 限制了什么？
9. `memory.create_task(...)` 是在哪个文件里实现的？
10. `self.tasks: dict[str, TaskRead]` 的 key 和 value 分别是什么？
11. `memory = MemoryStorage()` 为什么要放在文件底部创建一个共享对象？

