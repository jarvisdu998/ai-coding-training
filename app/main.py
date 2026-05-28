from contextlib import asynccontextmanager
from typing import Optional
from datetime import date
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用的生命周期管理器。在应用启动时自动初始化创建 SQLite 数据库表，
    并在关闭时进行必要的清理。
    """
    # 初始化创建所有 SQLAlchemy 实体对应的物理表
    models.Base.metadata.create_all(bind=engine)
    yield

# 创建 FastAPI 实例，定义文档说明，自动开启 OpenAPI 规范生成
app = FastAPI(
    title="RESTful Task Management API",
    description="基于 FastAPI + SQLite + SQLAlchemy 实现的任务管理后端 API",
    version="1.0.0",
    lifespan=lifespan
)

# 统一异常拦截器：处理输入校验失败 (HTTP 422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    自定义请求参数校验异常处理器，返回统一、标准化的错误 JSON。
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"][1:]),
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content={
            "message": "Input validation failed",
            "detail": errors
        }
    )

# 注册任务路由组，设置前缀 /api/v1/tasks
router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

@router.post("", response_model=schemas.TaskResponse, status_code=201)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    创建任务接口。
    如果参数校验（例如 title 超过100字符、状态值非法）不通过，将自动抛出 422 错误。
    """
    return crud.create_task(db=db, task_in=task_in)

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    按 ID 获取任务详情。如果任务不存在，抛出 404。
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """
    按 ID 更新现有任务。支持增量更新，如果任务不存在，抛出 404。
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, db_task=db_task, task_in=task_in)

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    按 ID 删除特定任务。如果任务不存在，抛出 404。
    删除成功返回 204 No Content。
    """
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task_by_id(db=db, db_task=db_task)
    return None

@router.get("", response_model=schemas.TaskListResponse)
def list_tasks(
    status: Optional[schemas.TaskStatus] = None,
    priority: Optional[schemas.TaskPriority] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = Query(0, ge=0, description="跳过的记录偏移量"),
    limit: int = Query(20, ge=1, le=100, description="单页最大记录数，取值 1-100"),
    sort_by: str = Query("created_at", description="排序字段，可选: created_at, priority, status, title"),
    sort_order: str = Query("desc", description="升降序，可选: asc, desc"),
    db: Session = Depends(get_db)
):
    """
    获取任务列表，支持多条件过滤（状态、优先级、创建时间区间）、排序与分页。
    """
    # 限制排序字段
    allowed_sort_fields = {"created_at", "priority", "status", "title"}
    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=422, 
            detail=f"Sorting by field '{sort_by}' is not supported. Supported: {allowed_sort_fields}"
        )
    
    # 限制排序顺序
    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=422, 
            detail="sort_order must be 'asc' or 'desc'"
        )

    items, total = crud.get_tasks_paginated(
        db=db,
        status=status,
        priority=priority,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }

# 注册子路由器
app.include_router(router)
