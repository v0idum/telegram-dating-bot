from mysql import connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import logging

log = logging.getLogger(__name__)


class DBConnector:

    def __init__(self, host, user, password, database):
        self.connection = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        try:
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(buffered=True)
        except Exception as e:
            log.error(str(e))

    def execute(self, sql, values=None):
        try:
            self.connection.ping(True, 5)
            self.cursor.execute(sql, values)
        except Exception as e:
            log.error('During executing: ' + str(e))

    def add_user(self, user_id, fullname, username, lan_code):
        sql = "INSERT INTO users (user_id, fullname, username, language_code) VALUES (%s, %s, %s, %s)"
        values = (user_id, fullname, username, lan_code)
        self.execute(sql, values)

    def update_user_data(self, user_id, name, age, gender, city, occupation, about, photo):
        sql = "UPDATE users SET name = %s, age = %s, gender = %s, \
                  city = %s, occupation = %s, about = %s, photo = %s, \
                  active = %s  \
                  WHERE user_id = %s"
        values = (name, age, gender, city, occupation, about, photo, 1, user_id)  # 1 is set to active state
        self.execute(sql, values)
        log.info(f'{name} joined')

    def add_fake(self, user_id, name, age, gender, city, occupation, about, photo):
        sql = "INSERT INTO users (user_id, name, age, gender, city, occupation, about, photo, active, is_fake) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.execute(sql, (user_id, name, age, gender, city, occupation, about, photo, 1, 1))  # Active and Fake
        log.info(f'Fake {name} added..')

    def is_fake(self, user_id):
        sql = "SELECT is_fake FROM users WHERE user_id = %s"
        self.execute(sql, (user_id,))
        return bool(self.cursor.fetchone()[0])

    def get_users(self):
        self.execute("SELECT user_id, name, age, gender, occupation FROM users WHERE active = 1 AND is_fake = 0")
        return self.cursor.fetchall()

    def next_user_by_city(self, city_id, gender, exclude, offset):
        sql = "SELECT \
                   users.user_id, users.name, users.age, cities.name, users.occupation, users.about, users.photo \
                   FROM users \
                   INNER JOIN cities ON users.city = cities.id \
                   WHERE \
                   users.active = 1 AND users.user_id != %s AND users.city = %s AND users.gender = %s AND \
                   NOT EXISTS(SELECT chat_id FROM chats WHERE ((chats.first_user = %s AND chats.second_user = users.user_id) OR \
                   (chats.first_user = users.user_id AND chats.second_user = %s)) AND chats.active = 1) \
                   LIMIT 2 OFFSET %s"
        self.execute(sql, (exclude, city_id, gender, exclude, exclude, offset))
        return self.cursor.fetchone()

    def get_user(self, user_id):
        sql = "SELECT \
                   users.user_id, users.name, users.age, cities.name, users.occupation, users.about, users.photo \
                   FROM users \
                   INNER JOIN cities ON users.city = cities.id\
                   WHERE users.user_id = %s"
        self.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def get_user_name(self, user_id):
        sql = "SELECT name \
                   FROM users \
                   WHERE user_id = %s"
        self.execute(sql, (user_id,))
        return self.cursor.fetchone()[0]

    def is_girl(self, user_id):
        sql = "SELECT gender FROM users WHERE user_id = %s"
        self.execute(sql, (user_id,))
        return not self.cursor.fetchone()[0]

    def is_banned(self, user_id):
        sql = "SELECT * FROM banned_users WHERE user_id = %s"
        self.execute(sql, (user_id,))
        return bool(self.cursor.fetchone())

    def ban_user(self, user_id):
        sql = "INSERT INTO banned_users (user_id) VALUES (%s)"
        self.execute(sql, (user_id,))

    def get_user_hearts(self, user_id):
        sql = "SELECT hearts FROM users WHERE user_id = %s"
        value = (user_id,)
        self.execute(sql, value)
        return self.cursor.fetchone()[0]

    def update_user_hearts(self, user_id, new_value):
        sql = "UPDATE users SET hearts = %s WHERE user_id = %s"
        values = (new_value, user_id)
        self.execute(sql, values)

    def user_exists(self, user_id):
        self.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return bool(len(self.cursor.fetchall()))

    def remove_user(self, user_id):
        sql = "DELETE FROM users WHERE user_id = %s"
        self.execute(sql, (user_id,))

    def update_user(self, user_id, field_to_update, new_value):
        sql = "UPDATE users SET {} = %s WHERE user_id = %s".format(field_to_update)
        self.execute(sql, (new_value, user_id))

    def is_user_active(self, user_id):
        self.execute("SELECT active FROM users WHERE user_id = %s", (user_id,))
        try:
            result = self.cursor.fetchone()[0]
        except TypeError:
            result = False
        return bool(result)

    def is_premium(self, user_id):
        self.execute("SELECT premium FROM users WHERE user_id = %s", (user_id,))
        return bool(self.cursor.fetchone()[0])

    def increase_referrals(self, user_id):
        increased_referrals = self.get_referrals(user_id) + 1
        self.execute("UPDATE users SET referrals = %s WHERE user_id = %s", (increased_referrals, user_id))

    def get_referrals(self, user_id):
        self.execute("SELECT referrals FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]

    def add_city(self, name):
        self.execute("INSERT INTO cities (name) VALUES (%s)", (name.capitalize(),))
        log.info(f'City {name} added')
        return self.cursor.lastrowid

    def city_exists(self, name):
        self.execute("SELECT * FROM cities WHERE name = %s", (name.capitalize(),))
        return bool(len(self.cursor.fetchall()))

    def get_city_id(self, name):
        if not self.city_exists(name):
            return self.add_city(name)

        self.execute("SELECT id FROM cities WHERE name = %s", (name,))
        return self.cursor.fetchone()[0]  # Returns id of the city

    def get_cities(self):
        self.execute("SELECT * FROM cities")
        return self.cursor.fetchall()

    def remove_city(self, name):
        sql = "DELETE FROM cities WHERE name = %s"
        self.execute(sql, (name.capitalize(),))

    def edit_users_city_name(self, city_id, new_name, old_name):
        new_city_id = self.get_city_id(new_name)
        sql = "UPDATE users SET city = %s WHERE city = %s"
        self.execute(sql, (new_city_id, city_id))
        self.remove_city(old_name)

    def create_chat(self, first_user, second_user):
        sql = "INSERT INTO chats (first_user, second_user) VALUES (%s, %s)"
        self.execute(sql, (first_user, second_user))
        chat_id = self.cursor.lastrowid
        self.add_chat_to_user(first_user, chat_id)

    def add_chat_to_user(self, user_id, chat_id):
        sql = "INSERT INTO users_chats (user_id, chat_id) VALUES (%s, %s)"
        self.execute(sql, (user_id, chat_id))

    def get_chats_of_user(self, user):
        sql = "SELECT c.first_user, c.second_user FROM chats AS c \
                   INNER JOIN users_chats AS uc ON c.chat_id = uc.chat_id \
                   WHERE uc.user_id = %s"
        self.execute(sql, (user,))
        return self.cursor.fetchall()

    def check_chat(self, user, with_whom):
        if not self.get_chat(user, with_whom):
            self.create_chat(user, with_whom)

    def get_chat(self, first, second):
        sql = "SELECT chat_id, first_user, second_user FROM chats \
                   WHERE (first_user = %s AND second_user = %s) OR (first_user = %s AND second_user = %s)"
        self.execute(sql, (first, second, second, first))
        return self.cursor.fetchone()

    def is_chat_active(self, chat_id):
        sql = "SELECT active FROM chats WHERE chat_id = %s"
        self.execute(sql, (chat_id,))
        return bool(self.cursor.fetchone()[0])

    def activate_chat(self, chat_id):
        sql = "UPDATE chats SET active = 1 WHERE chat_id = %s"
        self.execute(sql, (chat_id,))

    def add_like(self, who, whom):
        sql = "INSERT INTO users_likes (user_id, whom) VALUES (%s, %s)"
        self.execute(sql, (who, whom))

    def liked(self, who, whom):
        sql = "SELECT * FROM users_likes WHERE user_id = %s AND whom = %s"
        self.execute(sql, (who, whom))
        return bool(self.cursor.fetchone())

    def set_premium_expires_date(self, user_id, date):
        sql = "UPDATE users SET premium_expires = %s WHERE user_id = %s"
        self.execute(sql, (date, user_id))

    def get_premium_expires_date(self, user_id):
        sql = "SELECT premium_expires FROM users WHERE user_id = %s"
        self.execute(sql, (user_id,))
        return self.cursor.fetchone()[0]

    def close(self):
        self.connection.close()


db = DBConnector(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
