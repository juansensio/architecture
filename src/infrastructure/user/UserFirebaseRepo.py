from ..shared.FirebaseRepo import FirebaseRepo
from ...domain.user.user import User


class UserFirebaseRepo(FirebaseRepo):
    def __init__(self, name='todos', collection='users'):
        super().__init__(name)
        self.collection = collection

    def find_one_by_name(self, name):
        data = super().find_one_by_name(self.collection, 'username', name)
        return User(**data) if data else None

    def persist(self, data):
        return super().persist(self.collection, data['uid'], data)

    def add_todo(self, uid, todo_id):
        return super().add_item(self.collection, uid, 'todos', todo_id)

    def retrieve(self, id):
        return super().retrieve(self.collection, id)
