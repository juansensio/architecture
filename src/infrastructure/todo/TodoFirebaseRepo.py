from ..shared.FirebaseRepo import FirebaseRepo


class TodoFirebaseRepo(FirebaseRepo):
    def __init__(self, name='todos', collection='todos'):
        super().__init__(name)
        self.collection = collection

    def persist(self, data):
        return super().persist(self.collection, data['id'], data)

    def retrieve(self, id):
        return super().retrieve(self.collection, id)

    def update(self, data):
        return super().update(self.collection, data)

    def delete(self, id):
        return super().delete(self.collection, id)
