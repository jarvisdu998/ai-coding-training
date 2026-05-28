import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db

# 使用 SQLite 内存数据库作为测试环境，确保每次测试执行速度极快且数据完全隔离
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    针对每个独立的测试函数执行，都会生成一个崭新的数据库会话。
    在测试前自动建表，在测试后自动删表，从而保证完美的用例独立性。
    """
    # 1. 建立内存数据表结构
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # 2. 销毁内存数据表结构，清除痕迹
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    通过重写依赖注入，将 FastAPI 的 get_db 劫持并提供测试数据库 session。
    最后暴露 fastapi.testclient.TestClient 实例供测试断言使用。
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # 实施依赖劫持覆盖
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    # 测试用例执行完毕后，清除所有的覆盖，恢复原有配置
    app.dependency_overrides.clear()
