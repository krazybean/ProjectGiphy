import sqlite3
from projectgiphy import app
from projectgiphy.utilities.queries import sqlite

class SQLiteDB(object):

    def connect(self, app_context):
        try:
            conn = sqlite3.connect(app.database)
        except Exception as e:
            app.logger.exception(f"Error connecting to db: {app.database}")
            return
        return conn
        
        


if __name__ == '__main__':
    sdb = SQLiteDB()
    conn = sdb.connect(app)
    conn.execute(sqlite.create_table_avatars)
    conn.execute(sqlite.create_table_giphy_ratings)
    conn.execute(sqlite.create_table_roles)
    conn.execute(sqlite.create_table_tags)
    conn.execute(sqlite.create_table_users)
    conn.commit()
    conn.close()
    # TODO Add setup stuffs
