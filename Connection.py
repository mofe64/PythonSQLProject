from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os

load_dotenv()


class Connection:
    def __init__(self):
        self.conn = None
        self.__db_password = os.getenv("databasePassword")
        self.__db_user = os.getenv("databaseUser")
        self.__db_name = os.getenv("databaseName")
        self.connectionStatus = False

    def initialize_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user=self.__db_user,
                password=self.__db_password
            )
            print("DB connection successful ...")
            if self.conn.is_connected():
                self.connectionStatus = True
                sql = f'CREATE DATABASE IF NOT EXISTS {self.__db_name}'
                cursor = self.conn.cursor()
                cursor.execute(sql)
                self.use_current_db()
                self.create_table_on_first_initialization()
                return self.conn
        except Error as connectionError:
            print("Connection failed due to ", connectionError)

    def close_connection(self):
        if self.conn is not None and self.conn.is_connected:
            self.conn.close()
            self.connectionStatus = False
            print("Connection Closed ....")

    def create_table_on_first_initialization(self):
        queries = ['''CREATE TABLE IF NOT EXISTS Customer (
                    customerId INTEGER NOT NULL AUTO_INCREMENT,
                    firstName VARCHAR(120) NOT NULL,
                    lastname VARCHAR (120) NOT NULL,
                    middlename VARCHAR (120),
                    mobileNumber VARCHAR(20) UNIQUE NOT NULL,
                    occupation VARCHAR (40),
                    date_of_birth DATE,
                    constraint customer_pk PRIMARY KEY(customerId)
                    );
            ''',
                   '''
                       CREATE TABLE IF NOT EXISTS Account (
                           accountNumber INTEGER NOT NULL AUTO_INCREMENT,
                           customerId INTEGER NOT NULL,
                           accountType VARCHAR(50),
                           accountStatus VARCHAR(50),
                           accountOpeningDate DATE DEFAULT(CURRENT_DATE ),
                           constraint account_pk PRIMARY KEY(accountNumber),
                           constraint account_fk FOREIGN KEY(customerId) references Customer(customerId)
                           ON DELETE CASCADE 
                       );
                   ''',
                   '''
                       CREATE TABLE IF NOT EXISTS Transactions (
                           transactionId INTEGER NOT NULL  AUTO_INCREMENT,
                           accountNumber INTEGER NOT NULL,
                           transactionDate DATE DEFAULT (CURRENT_DATE ),
                           transactionType VARCHAR (30) NOT NULL,
                           transactionAmount INTEGER NOT NULL,
                           transactionMedium VARCHAR(50) NOT NULL,
                           constraint transactions_pk PRIMARY KEY(transactionId),
                           constraint transactions_fk FOREIGN KEY(accountNumber) references Account(accountNumber)
                           ON DELETE CASCADE 
                       );
                   ''',
                   ]
        cursor = self.conn.cursor()
        for query in queries:
            cursor.execute(query)

    def use_current_db(self):
        sql = f'Use {self.__db_name}'
        cursor = self.conn.cursor()
        cursor.execute(sql)

    # def get_cursor(self):
    #     return self.__cursor
    #
    # def get_connection(self):
    #     return self.__conn
    #
    # def get_dbname(self):
    #     return self.__db_name
    #
    # def get_connection_status(self):
    #     return self.__connectionStatus
