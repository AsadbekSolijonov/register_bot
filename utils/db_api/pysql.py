import logging
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)


class PySQL:
    def __init__(self):
        self.conn = sqlite3.connect(f'{BASE_DIR}/data_set.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        pass


class Register(PySQL):
    def create_table(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS  register (
        chat_id BIGINT NOT NULL,
        fullname TEXT,
        phone_number TEXT,
        lat REAL,
        lon REAL, 
        lang TEXT DEFAULT 'uz',
        PRIMARY KEY (chat_id));"""
        with self.conn:
            self.cursor.execute(sql_query)

    def insert(self,
               **kwargs):  # (chat_id=message.chat.id, fullname=fullname, phone_number=phone_number, lat=lat, lon=lon)
        cols = tuple(kwargs.keys())
        vals = tuple(kwargs.values())
        logging.info(f"{cols}, {vals}")
        sql_query = f"""
        INSERT INTO register {cols} VALUES {vals};
        """
        with self.conn:
            self.cursor.execute(sql_query)

    def update(self, chat_id, **kwargs):

        sql_query = f"""
        UPDATE register SET col1=val1, col2=val2 WHERE chat_id={chat_id};
        """


if __name__ == '__main__':
    Register()
    # pass
