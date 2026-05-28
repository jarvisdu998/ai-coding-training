from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import case
from sqlalchemy.orm import Session
from app import models, schemas

def get_task_by_id(db: Session, task_id: int) -> Optional[models.Task]:
    """
    根据任务 ID 查询单个任务
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_paginated(
    db: Session,
    status: Optional[schemas.TaskStatus] = None,
    priority: Optional[schemas.TaskPriority] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> Tuple[List[models.Task], int]:
    """
    带有多参数条件过滤、自定义排序和分页的列表查询。
    同时返回当前的记录列表和满足过滤条件的总记录数。
    """
    query = db.query(models.Task)

    # 1. 动态过滤条件
    if status is not None:
        query = query.filter(models.Task.status == status.value)
    
    if priority is not None:
        query = query.filter(models.Task.priority == priority.value)
        
    if start_date is not None:
        # 将 start_date date 转化为当天的起步时间 00:00:00.000000
        start_datetime = datetime.combine(start_date, datetime.min.time())
        query = query.filter(models.Task.created_at >= start_datetime)
        
    if end_date is not None:
        # 将 end_date date 转化为当天的最大时间 23:59:59.999999
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(models.Task.created_at <= end_datetime)

    # 计算符合过滤条件的总记录数（分页前）
    total = query.count()

    # 2. 动态自定义排序
    # 对于优先级（high > medium > low），使用 SQL CASE 表达式实现业务权重升降序，而非单纯的字母排序
    priority_case = case(
        (models.Task.priority == "high", 3),
        (models.Task.priority == "medium", 2),
        (models.Task.priority == "low", 1),
        else_=0
    )

    # 对于状态（done > in_progress > todo），同样支持权重排序
    status_case = case(
        (models.Task.status == "done", 3),
        (models.Task.status == "in_progress", 2),
        (models.Task.status == "todo", 1),
        else_=0
    )

    if sort_by == "priority":
        sort_field = priority_case
    elif sort_by == "status":
        sort_field = status_case
    else:
        # 默认或普通列反射（title, created_at 等）
        sort_field = getattr(models.Task, sort_by, models.Task.created_at)

    if sort_order == "asc":
        query = query.order_by(sort_field.asc())
    else:
        query = query.order_by(sort_field.desc())

    # 3. 分页切片
    items = query.offset(skip).limit(limit).all()

    return items, total

def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    """
    新建任务并持久化到数据库
    """
    db_task = models.Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status.value,
        priority=task_in.priority.value
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: models.Task, task_in: schemas.TaskUpdate) -> models.Task:
    """
    更新现有任务
    """
    # model_dump(exclude_unset=True) 可以只更新调用端明确传入的字段，保留未传字段不变
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            # 处理 Pydantic 枚举对象
            if hasattr(value, "value"):
                setattr(db_task, field, value.value)
            else:
                setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task_by_id(db: Session, db_task: models.Task) -> None:
    """
    从数据库中物理删除任务
    """
    db.delete(db_task)
    db.commit()
