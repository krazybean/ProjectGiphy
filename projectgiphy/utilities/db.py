import sqlite3
from projectgiphy import app
from projectgiphy.utilities.errors import *
from projectgiphy.utilities.queries import sqlite
from projectgiphy.utilities.tools import encrypt, decrypt

class SQLiteDB(object):

    def dict_factory(self, cursor, row):
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

    def get_users(self):
        try:
            r = self.conn.execute(sqlite.get_users)
            result = r.fetchall()
        except Exception:
            errmsg = "Error getting a list of users"
            app.logger.exception(GetUserListError(errmsg, ""))
        return None

    def get_user(self, username):
        r = self.conn.execute(sqlite.get_user, [username])
        result = r.fetchone()
        if result:
            return result
        return None

    def add(self):
        for attr in [self.username, self.password, self.email]:
            if not attr:
                raise MissingPersonAttributeError(f"Missing {attr}")
        password = encrypt('password', self.password)
        if self.get_user(self.username):
            app.logger.error(DuplicateUserError(f"User {self.username} already exists.", 'ERROR'))
            return
        try:
            self.conn.execute(sqlite.insert_user, [self.username,
                                                   self.email,
                                                   password,
                                                   'active', 2])
            self.conn.commit()
            app.logger.info(f"User {self.username} added")
            return "User added"
        except Exception:
            app.logger.exception(f"Unable to insert user {self.username}.")
            raise UserInsertionError(f"Failed to insert user {self.username}", app.logger.exception)

    def get_giphy(self, giphy_id):
        try:
            ir = self.conn.execute(sqlite.select_user_giphy, [self.username, giphy_id])
            return ir.fetchone()
        except Exception:
            errmsg = f"Image not found in db for {giphy_id} for user {self.username}"
            app.logger.error(ImageNotFoundError(errmsg))
        return None

    def get_all_giphys(self):
        try:
            r = self.conn.execute(sqlite.select_user_giphys, [self.username])
            return r.fetchall()
        except Exception:
            errmsg = f"Error finding images for user {self.username}"
            app.logger.error(errmsg)
        return None

    def get_tag(self, tag_name):
        try:
            r = self.conn.execute(sqlite.select_tag, [self.username, tag_name])
            return r.fetchone()
        except Exception:
            errmsg = f"Error searching for {tag_name} for {self.username}"
            app.logger.error(errmsg)
        return None

    def get_all_tags(self):
        try:
            r = self.conn.execute(sqlite.select_tags, [self.username])
            return r.fetchone()
        except Exception:
            errmsg = f"Error searching for tags for {self.username}"
            app.logger.error(errmsg)
        return None

    def add_tag_to_image(self, tag_id, giphy_id):
        user_details = self.get_user(self.username)
        user_id = user_details.get('id')
        try:
            self.conn.execute(sqlite.add_tag_to_image, [tag_id, giphy_id, user_id])
            self.conn.commit()
            return "Added tag to image"
        except Exception:
            errmsg = f"Failed to add tag {tag_id} to {giphy_id}"
            app.logger.exception(TagApplicationError(errmsg, ""))
            return errmsg

    def add_tag(self, tag_name, giphy_id=None):
        user_details = self.get_user(self.username)
        user_id = user_details.get('id')
        if self.get_tag(tag_name):
            errmsg = f"Error tag {tag_name} already exists for user {self.username}"
            app.logger.error(DuplicateTagError(errmsg, ""))
            return errmsg
        try:
            self.conn.execute(sqlite.create_tag, [tag_name, user_id])
            self.conn.commit()
            if giphy_id:
                tag = self.get_tag(tag_name)
                tag_id = tag.get('id')
                self.add_tag_to_image(tag_id, giphy_id)
                return f"Tag {tag_name} added."
        except Exception:
            errmsg = f"Failed to create tag {tag_name}"
            app.logger.exception(TagCreationError(errmsg, ""))


    def save_giphy(self, giphy_id, tag_id=None):
        user_details = self.get_user(self.username)
        if not user_details:
            errormsg = UserNotFoundError(f"No user found with username {self.username}", "")
            app.logger.error(errormsg)
            return errormsg
        user_id = user_details.get('id')
        if self.get_giphy(giphy_id):
            errmsg = f"image {giphy_id} already exists for {self.username}"
            app.logger.error(DuplicateImageError(errmsg, ""))
            return errmsg
        self.conn.execute(sqlite.insert_giphy_avatar, [user_id, giphy_id, tag_id])
        self.conn.commit()
        resp_msg = f"User image id {giphy_id} for {self.username} has been added"
        app.logger.info(resp_msg)
        return resp_msg

    def validate(self, password):
        try:
            encrypted = encrypt('password', password)
            r = self.conn.execute(sqlite.user_validate, [self.username, encrypted])
            result = r.fetchone()
        except Exception:
            errmsg = f"Error validating password for user {self.username}"
            app.logger.error(errmsg)
        if not result:
            return False
        return True


class Aux(object):
    def __init__(self):
        sdb = SQLiteDB()
        self.conn = sdb.connect(app)

    def get_ratings(self):
        try:
            r = self.conn.execute(sqlite.select_ratings)
            return r.fetchall()
        except Exception:
            app.logger.exception("Failed to pull ratings")
        return None

    def get_roles(self):
        try:
            r = self.conn.execute(sqlite.select_roles)
            return r.fetchall()
        except Exception:
            app.logger.exception("Failed to pull roles")
        return None




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
    aux = Aux()
    for role in sqlite.insert_role_data.splitlines():
        if not aux.get_roles():
            conn.execute(role)
    for rating in sqlite.insert_giphy_ratings.splitlines():
        if not aux.get_ratings():
            conn.execute(rating) 
    conn.commit()
    conn.close()
    # TODO Add setup stuffs

    # from flask import Flask
    # app = Flask(__name__)
    user = Users(username='testuser', email='test@test.com', password='test')
    user.add()
    user.save_giphy('12884939')
    user.add_tag('test', '12884939')
    user.add_tag('testing')
    print(user.validate('test1'))
