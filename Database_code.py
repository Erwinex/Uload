import pathlib
import sqlite3
import logging

PATH = pathlib.Path(__file__).parent.resolve()


class Database:

    def __init__(self) -> None:
        self._connect()
        self.make_users_table()
        self.make_chats_table()
        self.make_files_table()

    def _connect(self) -> None:
        try:
            self.conn = sqlite3.connect(f"{PATH}/database.db", check_same_thread=False)
            self._cur = self.conn.cursor()

        except Exception as e:
            logging.error('Database connection failed: ' + str(e))
            exit()

    def make_users_table(self) -> None:
        try:

            self._cur.execute(
                """CREATE TABLE IF NOT EXISTS users(
                num INTEGER PRIMARY KEY,
                tg_id TEXT UNIQUE,
                admin_rule TEXT);
                """)
            self.conn.commit()
        except Exception as e:
            logging.error('Table creation failed: ' + str(e))

    def insert_users(self, tel_id) -> bool:
        try:

            self._cur.execute(
                "INSERT INTO users(tg_id, admin_rule) VALUES(?,NULL);", [tel_id]
            )
            self.conn.commit()
            return True

        except Exception as e:
            logging.error('insert user data failed: ' + str(e))

    def select_admin_status(self, user_id):
        query = "SELECT admin_rule FROM users WHERE tg_id = ?;"

        self._cur.execute(query, [user_id])

        rows = self._cur.fetchone()
        self.conn.commit()
        return rows[0]

    def admins_list(self):
        query = "SELECT tg_id, admin_rule FROM users WHERE admin_rule IS NOT NULL ;"

        self._cur.execute(query)

        rows = self._cur.fetchall()
        self.conn.commit()
        return rows

    def add_admin(self, user_id):
        self.insert_users(user_id)
        query_1 = "UPDATE users SET admin_rule == ? WHERE tg_id = ?;"
        query_2 = "SELECT admin_rule FROM users WHERE tg_id = ?;"
        self._cur.execute(query_2, [str(user_id)])
        admin_status = self._cur.fetchone()
        if admin_status[0] == "owner":
            return False
            pass
        else:
            self._cur.execute(query_1, ["admin", str(user_id)])
            self.conn.commit()
            return True

    def remove_admin(self, user_id):
        query_1 = "UPDATE users SET admin_rule == ? WHERE tg_id = ?;"
        query_2 = "SELECT admin_rule FROM users WHERE tg_id = ?;"
        self._cur.execute(query_2, [str(user_id)])
        admin_status = self._cur.fetchone()
        if admin_status[0] == "owner":
            return False
            pass
        else:
            self._cur.execute(query_1, [None, user_id])
            self.conn.commit()
            return True

    def users_count(self):
        query = "SELECT COUNT(DISTINCT tg_id) FROM users;"
        self._cur.execute(query)
        count = self._cur.fetchone()
        self.conn.commit()
        print(count)
        return count[0]

    def select_users(self):
        query = "SELECT tg_id FROM users"

        self._cur.execute(query)

        rows = self._cur.fetchall()
        self.conn.commit()
        return rows

    '''
    def update_data(self, user_id):

        query = "UPDATE TABLE_NAME SET column1 == ? WHERE column2 = ?;"

        self._cur.execute(
            query, [user_id]
        )
        self.conn.commit()
        return True'''

    def make_chats_table(self) -> None:
        try:

            self._cur.execute(
                """CREATE TABLE IF NOT EXISTS chats(
                num INTEGER PRIMARY KEY,
                chat_id TEXT UNIQUE,
                chat_link TEXT UNIQUE);
                """)
            self.conn.commit()
        except Exception as e:
            logging.error('Table creation failed: ' + str(e))

    def insert_chats(self, chat_id, chat_link) -> bool:
        try:

            self._cur.execute(
                "INSERT INTO chats(chat_id, chat_link) VALUES(?, ?);", [chat_id, chat_link]
            )
            self.conn.commit()
            return True
        except Exception as e:
            logging.error('insert user data failed: ' + str(e))

    def select_chats(self):
        query = "SELECT chat_id, chat_link FROM chats;"

        self._cur.execute(query)

        rows = self._cur.fetchall()
        self.conn.commit()
        return rows

    def remove_chats(self, chat_id):
        query = "DELETE FROM chats WHERE chat_id=?;"

        self._cur.execute(query, [chat_id])

        '''rows = self._cur.fetchall()
        self.conn.commit()
        return rows'''

    def make_files_table(self) -> None:
        try:
            # file_id=message id
            self._cur.execute(
                """CREATE TABLE IF NOT EXISTS files(
                message_id TEXT,
                chat_id TEXT,
                file_id TEXT UNIQUE,
                downloads INTEGER);
                """)  # num INTEGER PRIMARY KEY,
            self.conn.commit()
        except Exception as e:
            logging.error('Table creation failed: ' + str(e))

    def insert_files(self, message_id, chat_id, file_id) -> bool:
        try:

            self._cur.execute(
                "INSERT INTO files(message_id, chat_id, file_id, downloads) VALUES(?,?,?,0);", [str(message_id),
                                                                                                   str(chat_id),file_id]
            )
            self.conn.commit()
            return True

        except Exception as e:
            logging.error('insert user data failed: ' + str(e))

    def select_files_data(self, file_id):
        query = "SELECT message_id, chat_id FROM files WHERE file_id = ?;"

        self._cur.execute(query, [file_id])

        rows = self._cur.fetchone()
        self.conn.commit()
        return rows

    def select_files_downloads(self, file_id):
        query = "SELECT downloads FROM files WHERE file_id = ?;"

        self._cur.execute(query, [file_id])

        rows = self._cur.fetchone()
        self.conn.commit()
        return rows[0]

    def update_files_downloads(self, file_id):
        query = "SELECT downloads FROM files WHERE file_id = ?;"

        self._cur.execute(query, [file_id])

        rows = self._cur.fetchone()

        query = "UPDATE files SET downloads == ? WHERE file_id = ?;"

        self._cur.execute(
            query, [int(rows[0])+1, file_id]
        )
        self.conn.commit()
        return True

    def remove_file(self, file_id):
        query = "DELETE FROM files WHERE chat_id=?;"

        self._cur.execute(query, [file_id])

    def close_db(self):
        self.conn.close()


db = Database()
