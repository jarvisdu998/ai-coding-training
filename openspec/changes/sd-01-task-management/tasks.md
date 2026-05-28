# Tasks: RESTful Task Management API

## Phase 1: 基础架构
- [x] Task 1.1: 建立项目依赖配置文件 requirements.txt 并初始化本地 Python 虚拟环境与激活
- [x] Task 1.2: 编写数据库连接配置模块 app/config.py 与 app/database.py，建立 SQLite 连接池并提供会话 Dependency

## Phase 2: 核心功能
- [x] Task 2.1: 编写 SQLAlchemy 数据表模型实体 app/models.py，映射 tasks 物理表 and 元数据定义
- [x] Task 2.2: 编写基于 Pydantic v2 的输入校验及出参模型 app/schemas.py，加入 Status/Priority 强枚举校验
- [x] Task 2.3: 编写核心数据库操作模块 app/crud.py，实现 CRUD、多条件联合过滤、升降序排序与 skip/limit 分页逻辑
- [x] Task 2.4: 编写 Web 入口层路由分发与统一异常处理器 app/main.py，关联端点并统一处理 Pydantic 校验与 404 错误响应

## Phase 3: 测试与优化
- [x] Task 3.1: 搭建单元与集成测试套件，在 tests/conftest.py 中配置内存 SQLite 并暴露测试客户端 Fixture
- [x] Task 3.2: 在 tests/test_tasks.py 中编写覆盖增删改查、多参数联合过滤、超限分页、边界排序以及异常格式的自动化用例，运行 pytest 确保 100% 通过
