class MemRepo():
    def __init__(self, data):
        self.data = data

    def find_one_by_field(self, field, name):
        try:
            user_ix = [u[field] for u in self.data].index(name)
            return self.data[user_ix]
        except:
            return None

    def persist(self, user):
        self.data.append(user)
        return user
