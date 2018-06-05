class MissingPersonAttributeError(Exception):
    def __init__(self, message, errors):
        super(MissingPersonAttributeError, self).__init__(message)
        self.errors = errors

class UserInsertionError(Exception):
    def __init__(self, message, errors):
        super(UserInsertionError, self).__init__(message)
        self.errors = errors

class UserNotFoundError(Exception):
    def __init__(self, message, errors):
        super(UserNotFoundError, self).__init__(message)
        self.errors = errors