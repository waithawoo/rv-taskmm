import pytest
from datetime import datetime

from src.modules.auth.services import AuthService
from src.modules.task.services import TaskService
from src.modules.auth.schemas import SingupModel
from src.modules.task.schemas import TaskCreateModel, TaskUpdateModel
from src.tests.conftest import UserTestModel, TaskTestModel


class TestServiceLevel:    
    @pytest.mark.asyncio
    async def test_authentication_service(self, db_session):
        """Test Authentication service - signup and login workflow"""
        auth_service = AuthService(UserTestModel)
        
        # Test user signup
        signup_data = SingupModel(
            name="Test User",
            email="test@example.com",
            password="securepassword123"
        )
        
        created_user = await auth_service.signup(db_session, signup_data)
        assert created_user is not None
        assert created_user.email == "test@example.com"
        assert created_user.name == "Test User"
        assert hasattr(created_user, 'id')
        
        # Test authentication with correct credentials
        authenticated_response = await auth_service.authenticate(
            db_session, "test@example.com", "securepassword123"
        )
        assert authenticated_response is not None
        assert authenticated_response['email'] == "test@example.com"
        assert 'access_token' in authenticated_response
        assert 'refresh_token' in authenticated_response
        
        # Test authentication with wrong password
        wrong_auth = await auth_service.authenticate(
            db_session, "test@example.com", "wrongpassword"
        )
        assert wrong_auth is None
    
    @pytest.mark.asyncio
    async def test_task_service_operations(self, db_session, test_user, test_admin_user):
        """Test Task service CRUD operations (service-level, no authorization)"""
        task_service = TaskService(TaskTestModel)
        
        # Test task creation
        task_data = TaskCreateModel(
            title="Service Test Task",
            description="This is a service-level test",
            status="TODO",
            priority="HIGH",
            creator_id=test_user.id,
            due_date=datetime(2024, 12, 31, 23, 59, 59)
        )
        
        created_task = await task_service.create(db_session, task_data, test_user)
        assert created_task is not None
        assert created_task.title == "Service Test Task"
        assert created_task.status == "TODO"
        assert created_task.creator_id == test_user.id
        
        # Test task update (service level allows any update)
        update_data = TaskUpdateModel(
            title="Updated Task Title",
            status="IN_PROGRESS"
        )
        
        updated_task = await task_service.update(
            db_session, created_task.id, update_data
        )
        assert updated_task.title == "Updated Task Title"
        assert updated_task.status == "IN_PROGRESS"
        
        # Test task retrieval
        found_task = await task_service.find(db_session, created_task.id)
        assert found_task is not None
        assert found_task.id == created_task.id
        
        # Test admin can delete any task (service level has no restrictions)
        deleted_task = await task_service.delete(db_session, created_task.id)
        assert deleted_task is not None
        
        # Verify task is deleted
        remaining_tasks = await task_service.list(db_session)
        assert not any(task.id == created_task.id for task in remaining_tasks)
