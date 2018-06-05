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

class DuplicateUserError(Exception):
    def __init__(self, message, errors):
        super(DuplicateUserError, self).__init__(message)
        self.errors = errors

class DuplicateImageError(Exception):
    def __init__(self, message, errors):
        super(DuplicateImageError, self).__init__(message)
        self.errors = errors

class ImageNotFoundError(Exception):
    def __init__(self, message, errors):
        super(ImageNotFoundError, self).__init__(message)
        self.errors = errors

class DuplicateTagError(Exception):
    def __init__(self, message, errors):
        super(DuplicateTagError, self).__init__(message)
        self.errors = errors

class TagCreationError(Exception):
    def __init__(self, message, errors):
        super(TagCreationError, self).__init__(message)
        self.errors = errors

class TagApplicationError(Exception):
    def __init__(self, message, errors):
        super(TagApplicationError, self).__init__(message)
        self.errors = errors

class GetUserListError(Exception):
    def __init__(self, message, errors):
        super(GetUserListError, self).__init__(message)
        self.errors = errors