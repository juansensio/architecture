import uuid


class MemRepo():
    def __init__(self, data):
        self.data = data

    def generate_id(self):
        return str(uuid.uuid4())

    def find_one_by_name(self, name, field):
        try:
            ix = [d[field] for d in self.data].index(name)
            return self.data[ix]
        except:
            return None

    def persist(self, data):
        return self.data.append(data)

    def exists(self, name, field='id'):
        return self.find_one_by_name(name, field) != None

    def retrieve(self, id, field='id'):
        return self.find_one_by_name(id, field)

    def update(self, data):
        ix = [d['id'] for d in self.data].index(data['id'])
        self.data[ix] = data
        return data

    def delete(self, id):
        ix = [d['id'] for d in self.data].index(id)
        self.data.pop(ix)
