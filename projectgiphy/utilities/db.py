import sqlite3
from projectgiphy import app
from projectgiphy.utilities.errors import *
from projectgiphy.utilities.queries import sqlite
from projectgiphy.utilities.tools import encrypt, decrypt

class SQLiteDB(object):
    """ Connection setup and cursor handback """

    def dict_factory(self, cursor, row):
        """ Dictonary factory used to return response in dict form

        Args:
            cursor (object): sqlite cursor object
            row (tuple): result set from query
        Returns:
            d (dict): dictonary representation of the data
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def connect(self, app_context):
        """ Connection using applicaiton context for globals

        Args:
            app_context (object): Flask object context
        Returns:
            conn (object): Sqlite cursory object
        """
        try:
            conn = sqlite3.connect(app.database)
            conn.row_factory = self.dict_factory
            return conn
        except Exception as e:
            app.logger.exception(f"Error connecting to db: {app.database}")
        return None


class Users(object):
    """ User construct with embedded operations """
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

    def get_user(self, username):
        """ Gets the user existance and records

        Args:
            username (str): Username
        Returns:
            result (dict): Dictionary representation of user details
        """
        r = self.conn.execute(sqlite.get_user, [username])
        result = r.fetchone()
        if result:
            return result
        return None

    def add(self):
        """ Add user object to database

        Args:
            None
        Returns:
            str
        """
        for attr in [self.username, self.password, self.email, self.avatar]:
            if not attr:
                raise MissingPersonAttributeError(f"Missing {attr}", "")
        password = encrypt('password', self.password)
        if self.get_user(self.username):
            app.logger.error(DuplicateUserError(f"User {self.username} already exists.", 'ERROR'))
            return
        try:
            self.conn.execute(sqlite.insert_user, [self.username,
                                                   self.email,
                                                   password,
                                                   'active',
                                                   2,
                                                   self.avatar])
            self.conn.commit()
            app.logger.info(f"User {self.username} added")
            return "User added"
        except Exception:
            app.logger.exception(f"Unable to insert user {self.username}.")
            raise UserInsertionError(f"Failed to insert user {self.username}", app.logger.exception)

    def get_giphy(self, giphy_id):
        """ gets a stored giphy based off of giphy_id

        Args:
            giphy_id (str): String of giphy_id number returned from api
        Returns:
            giphy_details (dict): Database storage of giphy meta-data
        """
        try:
            ir = self.conn.execute(sqlite.select_user_giphy, [self.username, giphy_id])
            return ir.fetchone()
        except Exception:
            errmsg = f"Image not found in db for {giphy_id} for user {self.username}"
            app.logger.error(ImageNotFoundError(errmsg))
        return None

    def get_all_giphys(self):
        """ gets all giphys associated with the user logged in

        Args:
            None
        Returns:
            dict: Dictonary dataset of all stored giphy under a signed in user
        """
        try:
            r = self.conn.execute(sqlite.select_user_giphys, [self.username])
            return r.fetchall()
        except Exception:
            errmsg = f"Error finding images for user {self.username}"
            app.logger.error(errmsg)
        return None

    def get_tag(self, tag_name):
        """ Gets a specific tag provided a tag_name

        Args:
            tag_name (str): Tag name to be searched
        Returns:
            dict: Dictonary dataset of a specific tag for a signed in user
        """
        try:
            r = self.conn.execute(sqlite.select_tag, [self.username, tag_name])
            return r.fetchone()
        except Exception:
            errmsg = f"Error searching for {tag_name} for {self.username}"
            app.logger.error(errmsg)
        return None

    def get_all_tags(self):
        """ Gets all tags under the user signed in

        Args:
            None
        Returns:
            dict: Dictonary list of all tags under the signed in user
        """
        try:
            r = self.conn.execute(sqlite.select_tags, [self.username])
            return r.fetchone()
        except Exception:
            errmsg = f"Error searching for tags for {self.username}"
            app.logger.error(errmsg)
        return None

    def add_tag_to_image(self, tag_id, giphy_id):
        """ Adds the tag provided to a given image

        Args:
            tag_id (int): Tag Primary Key to associate to a given image
            giphy_id (str): Indexed giphy ID in avatar to associate the tag with
        Returns:
            str: confirmation the update has occured
        """
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
        """ Adds a new tag

        Args:
            tag_name (str): Tag name to be represented
            giphy_id (str:optional): if provided associate the newly created tag
        Returns:
            str: Confirmation the tag has been created
        """
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


    def save_giphy(self, giphy_id, giphy_url=None, giphy_preview=None, tag_id=None):
        """ Saves the giphy image to the avatar table

        Args:
            giphy_id (str): ID of the giphy returned from the API
            giphy_url (str:optional): Url of the image location
            giphy_preview (str:optional): Url of the image preview
            tag_id (int:optional): Tag to associate to saved image
        Returns:
            str: Confirmation the image has been saved
        """
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
        self.conn.execute(sqlite.insert_giphy_avatar, [user_id, giphy_id, giphy_url, giphy_preview, tag_id])
        self.conn.commit()
        resp_msg = f"User image id {giphy_id} for {self.username} has been added"
        app.logger.info(resp_msg)
        return resp_msg

    def validate(self, password):
        """ Password validation (if we store password)

        Args:
            password (str): Unencrypted string to be encrypted and compared with whats saved
        Returns:
            bool: True or False given a match or not
        """
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
    """ Non user-specific associated calls """
    def __init__(self):
        sdb = SQLiteDB()
        self.conn = sdb.connect(app)

    def get_ratings(self):
        """ Gets a list of all ratings stored

        Args:
            None
        Returns:
            dict: Dictionary list of all giphy allowable ratings
        """
        try:
            r = self.conn.execute(sqlite.select_ratings)
            return r.fetchall()
        except Exception:
            app.logger.exception("Failed to pull ratings")
        return None

    def get_roles(self):
        """ User roles for administrative purposes

        Args:
            None
        Returns:
            dict: Dictionary list of all roles that exist
        """
        try:
            r = self.conn.execute(sqlite.select_roles)
            return r.fetchall()
        except Exception:
            app.logger.exception("Failed to pull roles")
        return None

    def get_users(self):
        """ Gets all users in the database

        Args:
            None
        Returns:
            dict: Dictionary list of all users that have been created
        """
        try:
            r = self.conn.execute(sqlite.get_users)
            result = r.fetchall()
            return result
        except Exception:
            errmsg = "Error getting a list of users"
            app.logger.exception(GetUserListError(errmsg, ""))
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

    # Testing bed
    user = Users(username='testuser', email='test@test.com', password='test', avatar='test')
    user.add()
    user.save_giphy('12884939', 'http://testurl', 'http://previewurl')
    user.add_tag('test', '12884939')
    user.add_tag('testing')
    print(user.validate('test1'))
