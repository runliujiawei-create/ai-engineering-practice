# engineering-agent

`engineering-agent` 是一个用于学习 Agent Engineering 的后端练习项目。

当前只实现 M0：Agent Backend Skeleton。这个阶段关注 Python 项目结构、FastAPI、HTTP API、Pydantic、Task / Run / Event、内存状态管理和 pytest。

## M0 实现内容

- 创建 Task
- 查询 Task
- 为 Task 创建一次 Run
- 使用 `DummyExecutor` 同步完成 Run
- 查询 Run
- 查询 Run 产生的 Events
- 使用内存中的 `dict` / `list` 保存状态
- 使用 pytest 覆盖核心 API 行为

## 项目结构

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
├── pyproject.toml
├── .gitignore
└── README.md
```

## 安装依赖

如果本机安装了 `uv`：

```bash
uv sync
```

如果没有安装 `uv`，可以使用 pip：

```bash
python -m pip install -e ".[dev]"
```

## 运行 FastAPI

```bash
uvicorn app.main:app --reload
```

默认访问：

```text
http://127.0.0.1:8000
```

交互式 API 文档：

```text
http://127.0.0.1:8000/docs
```

## 运行测试

```bash
pytest
```

## 当前没有实现

- LLM 推理
- Agent Loop
- Tool Calling
- 文件系统工具
- Shell / Python 执行工具
- MCP
- Human Approval
- Sandbox
- Tracing
- Evaluation
- 数据库
- Docker
- Authentication
- Frontend
- Message Queue
- Background Worker
- ORM
