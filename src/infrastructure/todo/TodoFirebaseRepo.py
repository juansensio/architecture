from ..shared.FirebaseRepo import FirebaseRepo
from ...domain.user.user import User


class TodoFirebaseRepo(FirebaseRepo):
    def __init__(self, name='todos', collection='users'):
        super().__init__(name)
        self.collection = collection

    def persist(self, data):
        return super().persist(self.collection, data['id'], data)
