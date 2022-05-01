import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_db(name):
    try:
        app = firebase_admin.get_app(name)
    except ValueError:
        cred = credentials.Certificate(
            "./infrastructure/shared/firebase.json")
        app = firebase_admin.initialize_app(cred, name=name)
    finally:
        return firestore.client(app)


class FirebaseRepo():
    def __init__(self, name="todos"):
        self.db = init_db(name)

    def find_one_by_name(self, collection, field, name):
        docs = list(self.db.collection(
            collection).where(field, "==", name).get())
        if len(docs) == 0:
            return None
        return docs[0].to_dict()

    def persist(self, collection, data):
        return self.db.collection(collection).add(data)