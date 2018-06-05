import sqlite3
from projectgiphy import app
from projectgiphy.utilities.errors import *
from projectgiphy.utilities.queries import sqlite

class SQLiteDB(object):

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self, app_context):
        try:
            conn = sqlite3.connect(app.database)
            conn.row_factory = self.dict_factory
            return conn
        except Exception as e:
            app.logger.exception(f"Error connecting to db: {app.database}")
        return None


class Users(object):
    def __init__(self,
                 username=None,
                 email=None,
                 password=None,
                 status=None,
                 avatar=None):
        self.username = username
        self.email = email
        self.password = password
        self.status = status
        self.avatar = avatar
        sdb = SQLiteDB()
        self.conn = sdb.connect(app)

    def add(self):
        for attr in [self.username, self.password, self.email]:
            if not attr:
                raise MissingPersonAttributeError(f"Missing {attr}")
        try:
            self.conn.execute(sqlite.insert_user, [self.username,
                                                   self.email,
                                                   self.password,
                                                   'active', 2])
            return "User added"
        except Exception:
            app.logger.exception(f"Unable to insert user {self.username}.")
            raise UserInsertionError(f"Failed to insert user f{self.username}")

    def save_giphy(self, giphy_id):
        self.conn.execute(sqlite.get_user, [self.username])
        result = self.conn.fetchone()
        if not result:
            raise UserNotFoundError




if __name__ == '__main__':
    sdb = SQLiteDB()
    # Construct tables
    conn = sdb.connect(app)
    conn.execute(sqlite.create_table_avatars)
    conn.execute(sqlite.create_table_giphy_ratings)
    conn.execute(sqlite.create_table_roles)
    conn.execute(sqlite.create_table_tags)
    conn.execute(sqlite.create_table_users)
    conn.commit()
    # Preseed data
    conn = sdb.connect(app)
    for role in sqlite.insert_role_data.splitlines():
        conn.execute(role)
    for rating in sqlite.insert_giphy_ratings.splitlines():
        conn.execute(rating) 
    conn.commit()
    conn.close()
    # TODO Add setup stuffs
