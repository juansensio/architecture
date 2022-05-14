import uuid


class MemRepo():
    def __init__(self, data):
        self.data = data

    def generate_id(self):
        return str(uuid.uuid4())

    def find_one_by_name(self, field, name):
        try:
            ix = [d[field] for d in self.data].index(name)
            return self.data[ix]
        except:
            return None

    def persist(self, data):
        return self.data.append(data)

    def exists(self, name, field='uid'):
        return self.find_one_by_name(name, field) != None
