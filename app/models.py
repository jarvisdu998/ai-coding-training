from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    """
    SQLAlchemy 任务实体模型类，映射数据库的 tasks 物理表。
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="todo")
    priority = Column(String(20), nullable=False, default="medium")
    
    # 使用数据库层面的当前时间戳作为默认值
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    # onupdate 会在每次 update 操作被触发时自动调用并生成最新系统时间
    updated_at = Column(
        DateTime, 
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now()
    )
