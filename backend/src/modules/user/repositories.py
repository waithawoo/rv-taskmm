from src.repositories import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model)
