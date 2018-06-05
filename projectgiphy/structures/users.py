from projectgiphy import app
from projectgiphy.utilities.db import Users
from projectgiphy.utilities.errors import *


class Person(object):

    def __init__(self,
                 username=None,
                 email=None,
                 password=None,
                 status=None):
        self.username = username
        self.email = email
        self.password = password
        self.status = status

    def add(self):
        for pattr in [self.username, self.email, self.password, self.status]:
            if not pattr:
                raise MissingPersonAttributeError(pattr)
        try:
            user = Users(username=self.username,
                        email=self.email,
                        password=self.password,
                        status=self.status)
        except Exception:
            app.logger.exception(f"Error inserting user {self.username}")
            raise UserInsertionError(self.username)
        return "User added"