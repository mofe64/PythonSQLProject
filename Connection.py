from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os

load_dotenv()


class Connection:
    def __init__(self):
        self.conn = None
        self.db_password = os.getenv("databasePassword")
        self.db_user = os.getenv("databaseUser")
        self.cursor = None

    def initialize_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user=self.db_user,
                password=self.db_password
            )
            print("DB connection successful ...")
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                sql = 'CREATE DATABASE IF NOT EXISTS nubari'
                self.cursor.execute(sql)
        except Error as connectionError:
            print("Connection failed due to ", connectionError)

    def close_connection(self):
        if self.conn is not None and self.conn.is_connected:
            self.conn.close()
            print("Connection Closed ....")

