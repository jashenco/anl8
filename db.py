import sqlite3
from encryption import encrypt_data

DB_NAME = 'fitplus.db'

class DBManager:
    """
    
    Usage:

    db = DBManager()
    db.create_tables()  # To create tables

    
    """
    _instance = None

    # Ensure Singleton pattern
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

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

    def select(self, query, params=()):
        cursor = None
        result = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            result = cursor.fetchone()
        except Exception as e:
            # TODO: Send exception to logs
            print("Error executing select: " + str(e))
        finally:
            self.close_db()
        return result

    def select_many(self, query, params=(), size=5):
        cursor = None
        results = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            results = cursor.fetchmany(size)
        except Exception as e:
            # TODO: Send exception to logs
            print("Error executing select_many: " + str(e))
        finally:
            self.close_db()
        return results

    def select_all(self, query, params=()):
        cursor = None
        results = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            results = cursor.fetchall()
        except Exception as e:
            # TODO: Send exception to logs
            print("Error executing select: " + str(e))
        finally:
            self.close_db()
        return results

    def modify(self, query, params=()):
        cursor = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            # TODO: Send exception to logs
            print("Error executing modify: " + str(e))
        finally:
            self.close_db()

    def create_tables(self):
        try:
            self.modify('''CREATE TABLE IF NOT EXISTS users
                                (user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, role TEXT, first_name TEXT, last_name TEXT, registration_date TEXT)''')
            
            self.modify('''CREATE TABLE IF NOT EXISTS members
                                (member_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, weight REAL, address TEXT, email TEXT, phone TEXT, registration_date TEXT)''')
            
            self.modify('''CREATE TABLE IF NOT EXISTS logs
                                (log_id INTEGER PRIMARY KEY, date TEXT, time TEXT, username TEXT, activity TEXT, additional_info TEXT, suspicious TEXT)''')

        except Exception as e:
            # TODO: Send exception to logs
            print("An error occurred while creating tables: " + str(e))

    def insert_super_admin(self, username = "SuperAdmin2", password = "password12"):
        try:
            password = encrypt_data(password)
            self.modify("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password, "Super Administrator"))
            return True

        except Exception as e:
            # TODO: Send exception to logs
            print("An error occurred while inserting super admin: " + str(e))

    # Display SQLite version for debugging
    def check_sqlite_version(self):
        version = self.select("SELECT sqlite_version()")
        print("SQLite version:", version[0])