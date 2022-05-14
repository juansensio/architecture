import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_db(name, creds="src/infrastructure/shared/firebase.json"):
    try:
        app = firebase_admin.get_app(name)
    except ValueError:
        cred = credentials.Certificate(creds)
        app = firebase_admin.initialize_app(cred, name=name)
    finally:
        return firestore.client(app)


class FirebaseRepo():
    def __init__(self, name="todos"):
        self.db = init_db(name)

    def generate_id(self):
        return self.db.collection(self.collection).document().id

    def find_one_by_name(self, collection, field, name):
        docs = list(self.db.collection(
            collection).where(field, "==", name).get())
        if len(docs) == 0:
            return None
        return docs[0].to_dict()

    def persist(self, collection, document, data):
        return self.db.collection(collection).document(document).set(data)

    def add_item(self, collection, document, field, item):
        return self.db.collection(collection).document(document).update({
            field: firestore.ArrayUnion([item])
        })
