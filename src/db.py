import sqlite3
from encryption import EncryptionManager
from mediator import EventHandler

DB_NAME = 'uniquemeal.db'

class DBManager:
    """
    Database Manager class to handle database operations.
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
        """
        Connect to the SQLite database.
        """
        try:
            self.conn = sqlite3.connect(DB_NAME)
            return self.conn.cursor()
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Database Connection Error", str(e), True))
            return None

    def close_db(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()

    def select(self, query, params=(), encrypt_indexes=[]):
        """
        Execute a SELECT query and return a single result.
        """
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
        """
        Execute a SELECT query and return multiple results.
        """
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
        """
        Execute a SELECT query and return all results.
        """
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

    def modify(self, query, params=(), encrypt_indexes=None, dry_run=False):
        """
        Execute an INSERT, UPDATE, or DELETE query with additional error handling.
        If dry_run is True, it will only validate the query without committing changes.
        """
        cursor = None
        try:
            cursor = self.connect_db()
            if encrypt_indexes:
                params_for_modification = [self._EncryptionManager.encrypt_data(param) if i in encrypt_indexes and isinstance(param, str) else param for i, param in enumerate(params)]
            else:
                params_for_modification = params

            self.conn.execute("BEGIN") # For dry run - so we can rollback after transaction

            # Execute the query
            cursor.execute(query, tuple(params_for_modification))

            if dry_run: # Rollback if dry run
                self.conn.rollback()
                return True
            else:
                # Commit if not dry run
                self.conn.commit()
                return True 

        except sqlite3.IntegrityError as e:
            self.conn.rollback()  # Roll back any changes if integrity error
            self.event_handler.emit("log_event", ("System", "Database Integrity Error", str(e), True))
            error_message = self._get_user_friendly_error(str(e))
            if dry_run:
                return False
            else:
                raise ValueError(error_message)

        except Exception as e:
            self.conn.rollback()  # Roll back any changes if error
            self.event_handler.emit("log_event", ("System", "Modify Query Error", str(e), True))
            if dry_run:
                return False
            else:
                raise ValueError("An unexpected database error occurred.")

        finally:
            self.close_db()

    def _get_user_friendly_error(self, error_message): # To generate error messages that do not reveal sensitive information
        """
        Convert database error messages to user-friendly messages.
        """
        if "UNIQUE constraint failed: users.username" in error_message:
            return "This username is already taken. Please choose a different one."
        elif "CHECK constraint failed: username" in error_message:
            return "Invalid username format. Username must be 8-10 characters long, start with a letter or underscore, and can contain letters, numbers, underscores, apostrophes, and periods."
        elif "CHECK constraint failed: password_hash" in error_message:
            return "Invalid password format. Password must be 12-30 characters long and include at least one lowercase letter, one uppercase letter, one digit, and one special character."
        elif "UNIQUE constraint failed: members.email" in error_message:
            return "This email is already registered. Please use a different email address."
        else:
            return "An error occurred while processing your request. Please check your input and try again."

    def create_tables(self):
        """
        Create the necessary database tables if they do not exist, with added constraints.
        """
        try:
            self.modify('''CREATE TABLE IF NOT EXISTS users
                                (user_id INTEGER PRIMARY KEY, 
                                username TEXT UNIQUE NOT NULL CHECK(
                                    length(username) BETWEEN 8 AND 10 AND
                                    username REGEXP '^[a-zA-Z_][a-zA-Z0-9_''.]{7,9}$'
                                ), 
                                password_hash TEXT NOT NULL CHECK(
                                    length(password_hash) BETWEEN 12 AND 30 AND
                                    password_hash REGEXP '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\(){}[\]:;''<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\(){}[\]:;''<>,.?/]{12,30}$'
                                ), 
                                role TEXT NOT NULL, 
                                first_name TEXT NOT NULL, 
                                last_name TEXT NOT NULL, 
                                registration_date TEXT NOT NULL)''')
            
            self.modify('''CREATE TABLE IF NOT EXISTS members
                                (member_id TEXT PRIMARY KEY, 
                                first_name TEXT NOT NULL, 
                                last_name TEXT NOT NULL, 
                                age INTEGER NOT NULL, 
                                gender TEXT NOT NULL, 
                                weight REAL NOT NULL, 
                                address TEXT NOT NULL, 
                                email TEXT UNIQUE NOT NULL, 
                                phone TEXT NOT NULL, 
                                registration_date TEXT NOT NULL)''')
            
            self.modify('''CREATE TABLE IF NOT EXISTS logs
                                (log_id INTEGER PRIMARY KEY, 
                                date TEXT NOT NULL, 
                                time TEXT NOT NULL, 
                                username TEXT NOT NULL, 
                                activity TEXT NOT NULL, 
                                additional_info TEXT, 
                                suspicious TEXT NOT NULL, 
                                read TEXT NOT NULL)''')
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Table Creation Error", str(e), True))

    def check_sqlite_version(self):
        """
        Display the SQLite version for debugging purposes.
        """
        version = self.select("SELECT sqlite_version()")
        print("SQLite version:", version[0])
