import sqlite3
from encryption import EncryptionManager
from mediator import EventHandler

DB_NAME = 'uniquemeal.db'

class DBManager:
    """
    Usage:
    db = DBManager()
    db.create_tables()  # To create tables
    """
    _instance = None

    # Ensure Singleton pattern
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            _EventHandler = EventHandler.get_instance()
            cls._instance = cls(_EventHandler)
            cls._instance.create_tables()
        return cls._instance

    def __init__(self, event_handler):
        self.conn = None
        self.event_handler = event_handler
        self._EncryptionManager = EncryptionManager(event_handler)

    def connect_db(self):
        try:
            self.conn = sqlite3.connect(DB_NAME)
            return self.conn.cursor()
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Database Connection Error", str(e), True))
            return None

    def close_db(self):
        if self.conn:
            self.conn.close()

    def select(self, query, params=(), encrypt_indexes=[]):
        cursor = None
        result = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            result = cursor.fetchone()
            if result:
                result = [self._EncryptionManager.decrypt_data(result[i]) if i in encrypt_indexes else result[i] for i in range(len(result))]
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Select Query Error", str(e), True))
        finally:
            self.close_db()
        return result

    def select_many(self, query, params=(), size=5, encrypt_indexes=[]):
        cursor = None
        results = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            results = cursor.fetchmany(size)
            if results:
                results = [[self._EncryptionManager.decrypt_data(result[i]) if i in encrypt_indexes else result[i] for i in range(len(result))] for result in results]
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Select Many Query Error", str(e), True))
        finally:
            self.close_db()
        return results

    def select_all(self, query, params=(), encrypt_indexes=[]):
        cursor = None
        results = None
        try:
            cursor = self.connect_db()
            cursor.execute(query, params)
            results = cursor.fetchall()
            if results:
                results = [[self._EncryptionManager.decrypt_data(result[i]) if i in encrypt_indexes else result[i] for i in range(len(result))] for result in results]
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Select All Query Error", str(e), True))
        finally:
            self.close_db()
        return results

    def modify(self, query, params=(), encrypt_indexes=None):
        #print("Modifying...")
        #print(query)
        #print(params)
        cursor = None
        try:
            cursor = self.connect_db()
            # Only encrypt parameters at specified indexes
            if encrypt_indexes:
                #print("Encrypting...")
                params_for_modification = [self._EncryptionManager.encrypt_data(param) if i in encrypt_indexes and isinstance(param, str) else param for i, param in enumerate(params)]
            else:
                params_for_modification = params
            #print(params_for_modification)
            cursor.execute(query, tuple(params_for_modification))
            self.conn.commit()
            #print('Inserted in db')
        except Exception as e:
            #print(e)
            self.event_handler.emit("log_event", ("System", "Modify Query Error", str(e), True))
        finally:
            self.close_db()

    def create_tables(self):
        try:
            self.modify('''CREATE TABLE IF NOT EXISTS users
                                (user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, role TEXT, first_name TEXT, last_name TEXT, registration_date TEXT)''')
            
            self.modify('''CREATE TABLE IF NOT EXISTS members
                                (member_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, weight REAL, address TEXT, email TEXT, phone TEXT, registration_date TEXT)''')
            
            self.modify('''CREATE TABLE IF NOT EXISTS logs
                                (log_id INTEGER PRIMARY KEY, date TEXT, time TEXT, username TEXT, activity TEXT, additional_info TEXT, suspicious TEXT, read TEXT)''')
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Table Creation Error", str(e), True))

    # Display SQLite version for debugging
    def check_sqlite_version(self):
        version = self.select("SELECT sqlite_version()")
        print("SQLite version:", version[0])
