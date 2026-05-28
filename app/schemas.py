from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="任务标题，非空且不能超过100字符")
    description: Optional[str] = Field(None, description="任务描述")
    status: TaskStatus = Field(TaskStatus.todo, description="任务状态")
    priority: TaskPriority = Field(TaskPriority.medium, description="任务优先级")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    # 所有字段均可选，但如果传入，title 必须满足非空且不超过 100 字符的规则
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    status: Optional[TaskStatus] = Field(None, description="任务状态")
    priority: Optional[TaskPriority] = Field(None, description="任务优先级")

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime

    # Pydantic v2 配置，使模型可以直接从 SQLAlchemy ORM 实例序列化
    model_config = {
        "from_attributes": True
    }

class TaskListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[TaskResponse]
