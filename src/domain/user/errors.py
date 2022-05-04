class UserAlreadyExistsError(Exception):
    def __init__(self):
        self.message = "User already exists"
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self):
        self.message = "User not found"
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    def __init__(self):
        self.message = "Invalid credentials"
        super().__init__(self.message)
