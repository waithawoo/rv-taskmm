from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Enum,
    Text,
    ForeignKey,
    TIMESTAMP,
    BigInteger
)
from sqlalchemy.orm import relationship, deferred

from src.models import Base

TaskStatus = Enum('TODO', 'IN_PROGRESS', 'DONE', name='task_status')
TaskPriority = Enum('LOW', 'MEDIUM', 'HIGH', name='task_priority')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(TaskStatus, nullable=False, default='TODO')
    priority = Column(TaskPriority, nullable=False, default='MEDIUM')
    due_date = Column(TIMESTAMP, nullable=True)
    assignee_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now)
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)

    assignee = relationship('User', back_populates='assigned_tasks', foreign_keys=[assignee_id])
    creator = relationship('User', back_populates='created_tasks', foreign_keys=[creator_id])
