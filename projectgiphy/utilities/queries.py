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
            "role_perm_matrices" TEXT NOT NULL
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
            "email" TEXT NOT NULL,
            "password" TEXT NOT NULL,
            "avatar_default_id" TEXT NOT NULL,
            "status" BOOLEAN,
            "role_id" INTEGER
            );
        """

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