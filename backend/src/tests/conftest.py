import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
from datetime import datetime

from src.models import Base
from src.modules.user.models import User
from src.modules.task.models import Task
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum


class UserTestModel(Base):
    __tablename__ = 'test_users'
    __sensitive_fields__ = {'password_hash'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False, default='USER')
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    deleted_at = Column(DateTime)

    @property
    def password(self):
        raise AttributeError('User.password is write-only')
    
    @password.setter
    def password(self, password):
        self.password_hash = self.generate_hash(password)
    
    def verify_password(self, password):
        from src.modules.auth.utils import verify_password
        return verify_password(password, self.password_hash)
    
    @staticmethod
    def generate_hash(password):
        from src.modules.auth.utils import generate_password_hash
        return generate_password_hash(password)


class TaskTestModel(Base):
    __tablename__ = 'test_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False, default='TODO')
    priority = Column(String, nullable=False, default='MEDIUM')
    due_date = Column(DateTime)
    assignee_id = Column(Integer, ForeignKey('test_users.id'))
    creator_id = Column(Integer, ForeignKey('test_users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    deleted_at = Column(DateTime)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_engine():
    """Create an in-memory SQLite async engine for testing"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("PRAGMA foreign_keys=ON"))
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def test_user(db_session):
    user = UserTestModel(
        name="Test User",
        email="test@example.com",
        role="USER"
    )
    user.password = "testpassword123"
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user


@pytest.fixture
async def test_admin_user(db_session):
    admin = UserTestModel(
        name="Admin User",
        email="admin@example.com",
        role="ADMIN"
    )
    admin.password = "adminpassword123"
    
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    return admin


@pytest.fixture
async def test_task(db_session, test_user):
    task = TaskTestModel(
        title="Test Task",
        description="This is a test task",
        status="TODO",
        priority="MEDIUM",
        creator_id=test_user.id,
        assignee_id=test_user.id,
        due_date=datetime(2024, 12, 31, 23, 59, 59)
    )
    
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    
    return task


@pytest.fixture
def mock_db_session():
    session = AsyncMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    return session
