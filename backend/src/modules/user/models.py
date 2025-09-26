from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Enum,
    TIMESTAMP,
    BigInteger
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, deferred

from src.models import Base
from src.modules.auth.utils import generate_password_hash, verify_password


ROLE = Enum('USER', 'ADMIN', name='user_role')


class User(Base):
    __tablename__ = 'users'
    __sensitive_fields__ = {'password_hash'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(ROLE, nullable=False, default='USER')
    password_hash = deferred(Column(String, nullable=False))
    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    
    assigned_tasks = relationship(
        'Task', back_populates='assignee', foreign_keys='Task.assignee_id'
    )
    created_tasks = relationship(
        'Task', back_populates='creator', foreign_keys='Task.creator_id'
    )

    @property
    def password(self):
        raise AttributeError('User.password is write-only')
    
    @password.setter
    def password(self, password):
        self.password_hash = self.generate_hash(password)
    
    def verify_password(self, password):
        return verify_password(password, self.password_hash)
    
    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password)
