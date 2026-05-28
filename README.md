# RESTful 任务管理 API (SD-01)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=Python&logoColor=white)](https://www.python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57.svg?style=flat&logo=SQLite&logoColor=white)](https://www.sqlite.org)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.3-0A9EDC.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org)
[![OpenSpec](https://img.shields.io/badge/OpenSpec-4%2F4%20Complete-brightgreen.svg?style=flat)](https://github.com/fission-ai/openspec)

基于 **FastAPI + SQLAlchemy 2.0 + SQLite** 实现的高性能、强校验、符合 RESTful 规范的任务管理系统（Task Management API）。本课题严格贯彻 **SDD (Spec-Driven Development，契约驱动开发)** 全生命周期开发流程。

---

## 📖 SDD 过程控制文档目录

本项目所有开发与设计规约均在 OpenSpec 框架内通过静态与动态校验：

*   **Proposal 提案 [Day 1]**：[`openspec/changes/sd-01-task-management/proposal.md`](./openspec/changes/sd-01-task-management/proposal.md) — 明确立项背景、实现目标及 Capabilities 范围判定。
*   **BDD 规约 Specs [Day 2]**：[`openspec/changes/sd-01-task-management/specs/task-api/spec.md`](./openspec/changes/sd-01-task-management/specs/task-api/spec.md) — 基于 `GIVEN-WHEN-THEN` 与 RFC 2119 标准（SHALL/MUST）声明的所有核心端点、数据校验及异常流程。
*   **System Design 系统设计 [Day 3]**：[`openspec/changes/sd-01-task-management/design.md`](./openspec/changes/sd-01-task-management/design.md) — 分层三层架构设计（API、Biz、Data）、SQLite 数据 Schema，以及基于 SQLAlchemy `case` 实现的权重自定义排序方案。
*   **Tasks 开发看板 [Day 3]**：[`openspec/changes/sd-01-task-management/tasks.md`](./openspec/changes/sd-01-task-management/tasks.md) — 拆细的原子开发进度控制看板。

---

## 🛠️ 技术选型与亮点

1.  **架构设计**：采用标准的 **API 接口层 (app/main.py)** ➔ **Biz 业务数据层 (app/crud.py)** ➔ **Models 实体建模层 (app/models.py)** 分层模式，解耦高内聚。
2.  **数据层**：基于现代化 Python 首选的 **SQLAlchemy 2.0** ORM 写法，利用 `connect_args={"check_same_thread": False}` 支持多线程并发。
3.  **高精度日期区间检索**：将用户传入的 `date` 对象（如 `2026-05-15`）无缝转化为当天的零点起止临界时间（`00:00:00.000000` 到 `23:59:59.999999`）进行 `DateTime` 闭区间检索，杜绝了时分秒丢失造成的“当天数据漏查”问题。
4.  **自定义权重排序**：利用数据库 `case` 语法对非字母序的优先级枚举进行权重硬编码（`high -> 3, medium -> 2, low -> 1`），完美支持了按紧急程度由高到低（`sort_by=priority&sort_order=desc`）的业务逻辑排序。
5.  **统一异常拦截**：通过覆写 FastAPI 的 `RequestValidationError`，当客户端传入空标题、非法枚举字符、非法页大小（skip/limit 参数超限）时，全局统一拦截并返回 `422 Unprocessable Entity` 格式的精美、高可读 JSON 报错信息。

---

## 📂 项目目录结构说明

```text
ai-coding-training/
├── app/
│   ├── __init__.py
│   ├── config.py         # 系统全局环境变量配置
│   ├── database.py       # 数据库引擎创建、连接池与 Session 工厂声明
│   ├── models.py         # SQLAlchemy 数据实体模型定义（tasks 物理表）
│   ├── schemas.py        # Pydantic v2 出入参强类型与枚举强校验定义
│   ├── crud.py           # 数据库核心动态 CRUD 操作（多条件联合过滤、自定义排序）
│   └── main.py           # FastAPI Web 路由注册与统一异常处理器入口
├── tests/
│   ├── conftest.py       # pytest 集成测试基础底座（内存 SQLite 强隔离环境、依赖覆盖）
│   └── test_tasks.py     # 18 组覆盖全场景、异常流的单元与集成测试用例
├── openspec/             # OpenSpec 契约驱动管理目录
├── requirements.txt      # 核心三方依赖明细
├── ai-coding-training-plan.md  # 培训实训大纲
└── README.md             # 本说明文档
```

---

## ⚡ 极速起步与部署指南

请确保本地电脑已安装 Python 3.10+ 环境。

### 1. 配置虚拟环境并安装依赖
```powershell
# 克隆仓库并进入根目录
git clone https://github.com/jarvisdu998/ai-coding-training.git
cd ai-coding-training

# 创建并激活虚拟环境 (Windows PowerShell)
python -m venv .venv
.venv\Scripts\activate

# 安装核心依赖包
pip install -r requirements.txt
```

### 2. 运行自动化测试集
```powershell
# 运行 pytest 自动化验证所有 Specs 定义的 BDD 场景
.venv\Scripts\python -m pytest -v
```

### 3. 运行本地 Web 服务
```powershell
# 启动本地 Uvicorn 服务，支持热重载
.venv\Scripts\uvicorn app.main:app --reload
```
服务成功启动后，你可以在浏览器中直接打开：
*   **交互式 API 文档 (Swagger UI)**: 👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*   **备用静态 API 文档 (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 自动化集成测试结果 (100% 通过率)

我们为所有 BDD 场景设计了高度自动化的用例，对接口展开了包含基本操作、多维联合检索、页边界及输入非法过滤在内的全场景渗透，在内存环境运行结果如下：

```text
============================= test session starts =============================
platform win32 -- Python 3.10.11, pytest-9.0.3, pluggy-1.6.0
cachedir: .pytest_cache
plugins: anyio-4.13.0
collected 18 items

tests/test_tasks.py::test_create_task_successfully PASSED                [  5%]
tests/test_tasks.py::test_create_task_invalid_data PASSED                [ 11%]
tests/test_tasks.py::test_get_existing_task_by_id PASSED                 [ 16%]
tests/test_tasks.py::test_get_non_existent_task PASSED                   [ 22%]
tests/test_tasks.py::test_update_task_successfully PASSED                [ 27%]
tests/test_tasks.py::test_update_non_existent_task PASSED                [ 33%]
tests/test_tasks.py::test_delete_task_successfully PASSED                [ 38%]
tests/test_tasks.py::test_delete_non_existent_task PASSED                [ 44%]
tests/test_tasks.py::test_filter_tasks_by_status_and_priority PASSED     [ 50%]
tests/test_tasks.py::test_filter_tasks_invalid_status_or_priority PASSED [ 55%]
tests/test_tasks.py::test_filter_tasks_by_creation_time_range PASSED     [ 61%]
tests/test_tasks.py::test_paginate_task_list_successfully PASSED         [ 66%]
tests/test_tasks.py::test_paginate_invalid_limit_or_skip PASSED          [ 72%]
tests/test_tasks.py::test_sort_task_list_ascending PASSED                [ 77%]
tests/test_tasks.py::test_sort_task_list_descending_priority PASSED      [ 83%]
tests/test_tasks.py::test_validation_invalid_status_in_creation PASSED   [ 88%]
tests/test_tasks.py::test_validation_invalid_priority_in_creation PASSED [ 94%]
tests/test_tasks.py::test_validation_title_too_long PASSED               [100%]

======================= 18 passed, 2 warnings in 0.35s ========================
```

---

## 🎬 交互式接口 Swagger UI 核心演示

通过在本地运行 Chrome 浏览器代理，我们在 Swagger UI 中针对核心 CRUD 和高级动态联合条件执行了完整的全流程演示，数据完美联动，交互页面极其现代 premium：

![Swagger UI 交互式动画](https://raw.githubusercontent.com/jarvisdu998/ai-coding-training/main/docs/api_swagger_demo.gif)

---

## 🤝 学习心得与 AI 协作复盘 (SDD 过程回顾)

*   **契约驱动开发的威力**：常规敏捷中常常会遇到实现与需求设计偏离。通过 OpenSpec 预先建立 `proposal` 和基于 GIVEN-WHEN-THEN 的 `spec.md` 契约，使编码时的接口签名、参数约束在开发初期就得以固化，使得后续 `main.py`、`crud.py` 等的实现效率极大提高。
*   **内存生命周期得失**：在使用 `sqlite:///:memory:` 进行单元测试时，遇到了连接归还导致数据库自动销毁的 `OperationalError` 经典坑。通过在 pytest Fixture 中巧妙配置 SQLAlchemy 的 `StaticPool`（静态共享连接池），完美解决了这个隐性 Bug，加深了对 SQLite 原生生命周期以及连接池底层管理的理解。
*   **AI 强协作效能**：通过先输入精确的 BDD specs 契约，AI 能够极其迅猛且以 100% 正确的数据映射结构（例如 Pydantic v2 的全新 `model_config = {"from_attributes": True}`）为我们一次性生成骨架及数据拦截处理器，极大地缩短了重复搬砖编码的时长，体现了 AI 辅助软件开发的巨大潜能！
