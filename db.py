import sqlite3

DB_NAME = 'fitplus.db'

class DBManager:
    """
    
    Usage:

    db = DBManager()
    db.create_tables()  # To create tables
    db.execute_query("INSERT INTO users (...) VALUES (...)", (value1, value2, ...))
    
    """

    def __init__(self):
        self.conn = None

    def connect_db(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            return self.conn.cursor()
        except Exception as e:
            # TODO: Send exception to logs
            print("An error occurred while connecting to the database: " + str(e))
            return None

    def close_db(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=()):
        cursor = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            self.conn.commit()
            return cursor
        except Exception as e:
            # TODO: Send exception to logs
            print("An error occurred while executing the query: " + str(e))
            return None
        finally:
            self.close_db()

    def create_tables(self):
        try:
            self.execute_query('''CREATE TABLE IF NOT EXISTS users
                                (user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, role TEXT, first_name TEXT, last_name TEXT, registration_date TEXT)''')
            
            self.execute_query('''CREATE TABLE IF NOT EXISTS members
                                (member_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, weight REAL, address TEXT, email TEXT, phone TEXT, registration_date TEXT)''')
            
            self.execute_query('''CREATE TABLE IF NOT EXISTS logs
                                (log_id INTEGER PRIMARY KEY, date TEXT, time TEXT, username TEXT, activity TEXT, additional_info TEXT, suspicious TEXT)''')
        except Exception as e:
            # TODO: Send exception to logs
            print("An error occurred while creating tables: " + str(e))

