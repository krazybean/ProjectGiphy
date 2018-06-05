class sqlite:
    create_table_avatars = """
        CREATE TABLE IF NOT EXISTS "avatars" (
            "id" INTEGER CONSTRAINT "pk_avatars" PRIMARY KEY AUTOINCREMENT,
            "person_id" INTEGER,
            "giphy_id" TEXT NOT NULL,
            "tag_id" INTEGER
        );
        """

    create_table_giphy_ratings = """
        CREATE TABLE IF NOT EXISTS "giphy_rating" (
            "id" INTEGER CONSTRAINT "pk_giphy_rating" PRIMARY KEY AUTOINCREMENT,
            "rating_name" TEXT NOT NULL,
            "rating_definition" TEXT NOT NULL
        );
        """

    create_table_roles = """
        CREATE TABLE IF NOT EXISTS "roles" (
            "id" INTEGER CONSTRAINT "pk_roles" PRIMARY KEY AUTOINCREMENT,
            "role_name" TEXT NOT NULL,
            "role_perm_matrices" TEXT
        );
        """

    create_table_tags = """
        CREATE TABLE IF NOT EXISTS "tags" (
            "id" INTEGER CONSTRAINT "pk_tags" PRIMARY KEY AUTOINCREMENT,
            "tag_name" TEXT NOT NULL,
            "person_id" INTEGER
        );
        """

    create_table_users = """
        CREATE TABLE IF NOT EXISTS "users" (
            "id" INTEGER CONSTRAINT "pk_users" PRIMARY KEY AUTOINCREMENT,
            "username" TEXT NOT NULL,
            "email" TEXT,
            "password" TEXT,
            "avatar_default_id" TEXT,
            "status" BOOLEAN,
            "role_id" INTEGER
        );
        """

    select_roles = """ SELECT role_name FROM roles; """

    insert_role_data = """
        INSERT INTO roles (role_name, role_perm_matrices) VALUES ('Admin', Null);
        INSERT INTO roles (role_name, role_perm_matrices) VALUES ('User', Null);
    """


    select_ratings = """ SELECT rating_name, rating_definition FROM giphy_rating; """

    insert_giphy_ratings = """
        INSERT INTO giphy_rating (rating_name, rating_definition) VALUES ('y', "Youth approved");
        INSERT INTO giphy_rating (rating_name, rating_definition) VALUES ('g', "General Audience");
        INSERT INTO giphy_rating (rating_name, rating_definition) VALUES ('pg', "Parental Guidance Suggested");
        INSERT INTO giphy_rating (rating_name, rating_definition) VALUES ('pg-13', "Parents Strongly Cautioned");
        INSERT INTO giphy_rating (rating_name, rating_definition) VALUES ('r', "Restricted");
    """


    # User operations
    get_users = """ SELECT u.username, u.email, u.status, r.role_name
                    FROM users u
                    INNER JOIN roles r
                    ON u.role_id = r.id; """

    get_user = """ SELECT u.id, u.username, u.email, u.status, r.role_name
                   FROM users u
                   INNER JOIN roles r
                   ON u.role_id = r.id
                   WHERE u.username = ?; """

    user_validate = """ SELECT password FROM users WHERE username = ? and password = ?;"""

    insert_user = """ INSERT INTO users (username, email, password, status, role_id) VALUES (?, ?, ?, ?, ?); """

    update_user_password = """ UPDATE users SET password = ? WHERE username = ?; """

    update_user_status = """ UPDATE users SET status = ? WHERE username = ?; """

    delete_user = """ DELETE FROM users WHERE username = ?; """

    select_roles = """ SELECT role_name FROM roles; """

    insert_giphy_avatar = """ INSERT INTO avatars (person_id, giphy_id, tag_id) VALUES (?, ?, ?); """

    select_user_giphys = """ SELECT u.username, a.giphy_id, a.tag_id
                             FROM avatars a
                             INNER JOIN users u
                             ON a.person_id = u.id
                             WHERE u.username = ?; """

    select_user_giphy = """ SELECT u.username, a.giphy_id, a.tag_id
                            FROM avatars a
                            INNER JOIN users u
                            ON a.person_id = u.id
                            WHERE u.username = ?
                            AND a.giphy_id = ?; """

    create_tag = """ INSERT INTO tags (tag_name, person_id) VALUES (?, ?);"""

    add_tag_to_image = """ UPDATE avatars SET tag_id = ? WHERE giphy_id = ? AND person_id = ?;"""

    select_tags = """ SELECT t.id, t.tag_name
                      FROM tags t
                      INNER JOIN users u
                      ON t.person_id = u.id
                      WHERE u.person_id = ?;"""

    select_tag = """ SELECT t.id, t.tag_name
                     FROM tags t
                     INNER JOIN users u
                     ON t.person_id = u.id
                     WHERE u.username = ?
                     AND t.tag_name = ?;"""


class mysql:
    create_table_avatars = """
        CREATE TABLE IF NOT EXISTS `avatars` (
            `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
            `person_id` INTEGER,
            `giphy_id` VARCHAR(255) NOT NULL,
            `tag_id` INTEGER
        );
        """

    create_table_giphy_ratings = """
        CREATE TABLE IF NOT EXISTS `giphy_rating` (
            `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
            `rating_name` VARCHAR(255) NOT NULL,
            `rating_definition` VARCHAR(255) NOT NULL
        );
        """

    create_table_roles = """
        CREATE TABLE IF NOT EXISTS `roles` (
            `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
            `role_name` VARCHAR(255) NOT NULL,
            `role_perm_matrices` VARCHAR(255) NOT NULL
        );
        """

    create_table_tags = """
        CREATE TABLE IF NOT EXISTS `tags` (
            `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
            `tag_name` VARCHAR(255) NOT NULL,
            `person_id` INTEGER
        );
        """

    create_table_users = """
        CREATE TABLE IF NOT EXISTS `users` (
            `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
            `username` VARCHAR(255) NOT NULL,
            `email` VARCHAR(255) NOT NULL,
            `password` VARCHAR(255) NOT NULL,
            `avatar_default_id` VARCHAR(255) NOT NULL,
            `status` BOOLEAN,
            `role_id` INTEGER
        );
        """


class postgres():
    create_table_avatars = """
        CREATE TABLE IF NOT EXISTS "avatars" (
            "id" SERIAL CONSTRAINT "pk_avatars" PRIMARY KEY,
            "person_id" INTEGER,
            "giphy_id" TEXT NOT NULL,
            "tag_id" INTEGER
        );
        """

    create_table_giphy_ratings = """
        CREATE TABLE IF NOT EXISTS "giphy_rating" (
            "id" SERIAL CONSTRAINT "pk_giphy_rating" PRIMARY KEY,
            "rating_name" TEXT NOT NULL,
            "rating_definition" TEXT NOT NULL
        );
        """

    create_table_roles = """
        CREATE TABLE IF NOT EXISTS "roles" (
            "id" SERIAL CONSTRAINT "pk_roles" PRIMARY KEY,
            "role_name" TEXT NOT NULL,
            "role_perm_matrices" TEXT NOT NULL
        );
        """

    create_table_tags = """
        CREATE TABLE IF NOT EXISTS "tags" (
            "id" SERIAL CONSTRAINT "pk_tags" PRIMARY KEY,
            "tag_name" TEXT NOT NULL,
            "person_id" INTEGER
        );
        """

    create_table_users = """
        CREATE TABLE IF NOT EXISTS "users" (
            "id" SERIAL CONSTRAINT "pk_users" PRIMARY KEY,
            "username" TEXT NOT NULL,
            "email" TEXT NOT NULL,
            "password" TEXT NOT NULL,
            "avatar_default_id" TEXT NOT NULL,
            "status" BOOLEAN,
            "role_id" INTEGER
        );
        """