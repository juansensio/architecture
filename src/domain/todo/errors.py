class TodoNotFoundError(Exception):
    def __init__(self):
        self.message = "Todo not found"
        super().__init__(self.message)
