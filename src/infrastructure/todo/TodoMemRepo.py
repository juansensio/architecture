from ..shared.MemRepo import MemRepo


class TodoMemRepo(MemRepo):
    def __init__(self, data=[]):
        self.data = data
