from src.modules.auth.routes import AuthRoute
from src.modules.user.routes import UserRoute
from src.modules.task.routes import TaskRoute

__all__ = ['routes']

routes = [
    AuthRoute().base,
    UserRoute().base,
    TaskRoute().base,
]
