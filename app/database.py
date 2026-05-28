from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLite 数据库特殊参数：check_same_thread=False 允许在多个线程中共享同一个数据库会话
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    提供给 FastAPI Depends 依赖注入的数据库会话生成器。
    确保每次请求结束后，数据库连接能被正确关闭释放。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
