import pytest
from datetime import datetime
from app.models import Task

# ==========================================
# 1. 任务 CRUD 功能测试场景
# ==========================================

def test_create_task_successfully(client):
    """
    正常流：成功创建一个合格的任务，返回 201 状态码，并校验返回的属性和 ID
    """
    payload = {
        "title": "Learn FastAPI",
        "description": "Read all specifications and write code",
        "status": "todo",
        "priority": "high"
    }
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert data["title"] == payload["title"]
    assert data["status"] == "todo"
    assert data["priority"] == "high"
    assert "created_at" in data
    assert "updated_at" in data

def test_create_task_invalid_data(client):
    """
    异常流：创建任务时标题为空或字段缺失，应被 Pydantic 拒绝并返回 422
    """
    # 场景 1：缺失 required 标题字段
    payload_missing_title = {
        "description": "No title provided",
        "priority": "low"
    }
    response = client.post("/api/v1/tasks", json=payload_missing_title)
    assert response.status_code == 422
    assert "detail" in response.json()

    # 场景 2：标题为空字符串（触发 min_length=1 约束）
    payload_empty_title = {
        "title": "",
        "description": "Empty string title",
        "status": "todo"
    }
    response = client.post("/api/v1/tasks", json=payload_empty_title)
    assert response.status_code == 422

def test_get_existing_task_by_id(client):
    """
    正常流：获取数据库中已存在任务的详情，返回 200
    """
    # 先创建一个任务
    create_res = client.post("/api/v1/tasks", json={"title": "Target Task"})
    task_id = create_res.json()["id"]

    # 查询详情
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Target Task"
    assert response.json()["id"] == task_id

def test_get_non_existent_task(client):
    """
    异常流：获取不存在的 ID，系统应统一拦截并抛出 404 Standard Error
    """
    response = client.get("/api/v1/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_update_task_successfully(client):
    """
    正常流：修改已存在任务的部分或全部字段，返回 200 且数据更新
    """
    create_res = client.post("/api/v1/tasks", json={"title": "Old Task", "priority": "low"})
    task_id = create_res.json()["id"]

    # 提交部分修改
    update_payload = {
        "title": "New Title",
        "status": "in_progress",
        "priority": "high"
    }
    response = client.put(f"/api/v1/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"

def test_update_non_existent_task(client):
    """
    异常流：对不存在的任务发起修改，应返回 404
    """
    response = client.put("/api/v1/tasks/99999", json={"title": "Updated Task"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task_successfully(client):
    """
    正常流：成功删除已存在的任务，返回 204。再次查询该任务应返回 404
    """
    create_res = client.post("/api/v1/tasks", json={"title": "To Be Deleted"})
    task_id = create_res.json()["id"]

    # 执行删除
    del_res = client.delete(f"/api/v1/tasks/{task_id}")
    assert del_res.status_code == 204
    assert del_res.content == b"" # 204 No Content 不应有 Body

    # 验证确实被物理删除
    get_res = client.get(f"/api/v1/tasks/{task_id}")
    assert get_res.status_code == 404

def test_delete_non_existent_task(client):
    """
    异常流：对不存在的任务发起删除，应返回 404
    """
    response = client.delete("/api/v1/tasks/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


# ==========================================
# 2. 多条件动态过滤测试场景
# ==========================================

def test_filter_tasks_by_status_and_priority(client):
    """
    正常流：根据任务的状态和优先级联合过滤任务列表
    """
    # 填充各种状态的任务
    client.post("/api/v1/tasks", json={"title": "Task 1", "status": "todo", "priority": "low"})
    client.post("/api/v1/tasks", json={"title": "Task 2", "status": "in_progress", "priority": "high"})
    client.post("/api/v1/tasks", json={"title": "Task 3", "status": "in_progress", "priority": "high"})
    client.post("/api/v1/tasks", json={"title": "Task 4", "status": "done", "priority": "high"})

    # 发起多条件过滤查询
    response = client.get("/api/v1/tasks?status=in_progress&priority=high")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for item in data["items"]:
        assert item["status"] == "in_progress"
        assert item["priority"] == "high"

def test_filter_tasks_invalid_status_or_priority(client):
    """
    异常流：使用非法的 status 值或 priority 过滤列表，应返回 422 校验失败
    """
    res1 = client.get("/api/v1/tasks?status=unknown")
    assert res1.status_code == 422

    res2 = client.get("/api/v1/tasks?priority=critical")
    assert res2.status_code == 422

def test_filter_tasks_by_creation_time_range(client, db_session):
    """
    正常流：通过设置起止日期 (start_date/end_date) 闭区间过滤特定创建时间的任务。
    我们直接操作 db_session 绕过系统时间的即时自动填充。
    """
    # 显式构造不同创建时间的任务并存入数据库
    t1 = Task(title="May Task", status="todo", priority="medium", created_at=datetime(2026, 5, 15, 10, 0, 0))
    t2 = Task(title="June Task", status="todo", priority="medium", created_at=datetime(2026, 6, 5, 15, 30, 0))
    db_session.add_all([t1, t2])
    db_session.commit()

    # 场景 1：查询 5 月范围内的任务，应当只返回 May Task
    response = client.get("/api/v1/tasks?start_date=2026-05-01&end_date=2026-05-31")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "May Task"


# ==========================================
# 3. 分页与排序功能测试场景
# ==========================================

def test_paginate_task_list_successfully(client):
    """
    正常流：分页查询，传入 skip 和 limit 控制获取条数并带回准确的匹配总数
    """
    # 填充 8 个任务
    for i in range(8):
        client.post("/api/v1/tasks", json={"title": f"Batch Task {i}"})

    # 查询第一页（5条记录）
    response = client.get("/api/v1/tasks?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 8
    assert len(data["items"]) == 5
    assert data["skip"] == 0
    assert data["limit"] == 5

def test_paginate_invalid_limit_or_skip(client):
    """
    异常流：传入负值分页参数，或传入超限的 limit（如 500），应返回 422
    """
    # 场景 1：limit 为负数
    res1 = client.get("/api/v1/tasks?limit=-5")
    assert res1.status_code == 422

    # 场景 2：limit 大于允许的上限值 100
    res2 = client.get("/api/v1/tasks?limit=500")
    assert res2.status_code == 422

def test_sort_task_list_ascending(client, db_session):
    """
    正常流：按创建时间升序 (asc) 排序列表
    """
    t1 = Task(title="Early Task", created_at=datetime(2026, 1, 1))
    t2 = Task(title="Late Task", created_at=datetime(2026, 12, 31))
    db_session.add_all([t1, t2])
    db_session.commit()

    response = client.get("/api/v1/tasks?sort_by=created_at&sort_order=asc")
    assert response.status_code == 200
    items = response.json()["items"]
    assert items[0]["title"] == "Early Task"
    assert items[1]["title"] == "Late Task"

def test_sort_task_list_descending_priority(client):
    """
    正常流：自定义排序测试。按优先级由高到低降序 (desc) 排序，应遵循 high > medium > low 的自定义规则
    """
    client.post("/api/v1/tasks", json={"title": "Medium Task", "priority": "medium"})
    client.post("/api/v1/tasks", json={"title": "High Task", "priority": "high"})
    client.post("/api/v1/tasks", json={"title": "Low Task", "priority": "low"})

    response = client.get("/api/v1/tasks?sort_by=priority&sort_order=desc")
    assert response.status_code == 200
    items = response.json()["items"]
    
    # 严格验证排序权重符合：High (0) -> Medium (1) -> Low (2)
    assert items[0]["title"] == "High Task"
    assert items[1]["title"] == "Medium Task"
    assert items[2]["title"] == "Low Task"


# ==========================================
# 4. 输入格式深度校验测试场景
# ==========================================

def test_validation_invalid_status_in_creation(client):
    """
    异常流：传入不存在的任务状态（e.g. 'not_started'），系统应返回 422 提示只能是 'todo', 'in_progress', 'done'
    """
    payload = {"title": "Task", "status": "not_started"}
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 422
    assert "status" in response.json()["detail"][0]["field"]

def test_validation_invalid_priority_in_creation(client):
    """
    异常流：传入不存在的任务优先级（e.g. 'critical'），系统应返回 422 提示范围限制
    """
    payload = {"title": "Task", "priority": "critical"}
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 422
    assert "priority" in response.json()["detail"][0]["field"]

def test_validation_title_too_long(client):
    """
    异常流：传入超过 100 字符的标题，应拦截返回 422 报错
    """
    long_title = "A" * 101
    payload = {"title": long_title}
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["field"]
