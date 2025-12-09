import sys
sys.dont_write_bytecode = True

import os
import dotenv
import pymysql

class Connection:
    def __init__(self):
        dotenv.load_dotenv()

        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_DATABASE = os.getenv("DB_DATABASE")
        DB_PORT = int(os.getenv("DB_PORT", default=3306))

        self.connect_db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_DATABASE,
            port=DB_PORT
        )
        self.cur = self.connect_db.cursor()