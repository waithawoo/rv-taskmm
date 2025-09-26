from src.repositories import BaseRepository


class TaskRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)
