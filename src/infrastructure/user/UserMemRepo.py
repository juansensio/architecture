from ..shared.MemRepo import MemRepo
from ...domain.user.user import User


class UserMemRepo(MemRepo):
    def __init__(self, data=[]):
        self.data = data

    def find_one_by_name(self, name):
        data = super().find_one_by_name('username', name)
        return User(**data) if data else None
