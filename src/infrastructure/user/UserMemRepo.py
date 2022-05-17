from ..shared.MemRepo import MemRepo
from ...domain.user.user import User


class UserMemRepo(MemRepo):
    def __init__(self, data=[]):
        self.data = data

    def find_one_by_name(self, name, field="username"):
        data = super().find_one_by_name(name, field)
        return User(**data) if data else None

    def add_todo(self, uid, todo_id):
        for user in self.data:
            if user['uid'] == uid:
                user['todos'].append(todo_id)
                break

    def remove_todo(self, uid, todo_id):
        for user in self.data:
            if user['uid'] == uid:
                user['todos'].remove(todo_id)
                break

    def retrieve(self, id):
        return super().retrieve(id, field='uid')

    def exists(self, uid):
        return super().exists(uid, field='uid')
