from db import DBManager
from encryption import encrypt_data
import datetime


class Logger:
    _instance = None  

    @classmethod
    def get_instance(cls):
        """
        Singleton class to ensure only one instance of the Logger class is created.
        Is called on the class itself rather than a function of the class (cls)
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """
        Constructor for the Logger class.
        """
        if self._instance:
            raise Exception("You cannot create another Logger class!")
        
        self.failed_login_attempts = {}
        self.recent_deletions = []
        self.recent_role_changes = []
        self._db_manager = DBManager()

    def log_activity(self, username, description, additional_info, suspicious=None):
        """
        Log the activity to the database.
        """
        date = str(datetime.date.today())
        time = str(datetime.datetime.now().time())[:8]
        
        encrypted_description = encrypt_data(description)
        encrypted_additional_info = encrypt_data(additional_info)

        if suspicious is None:
            suspicious = "Yes" if self.flag_suspicious_activity(username, description) else "No"
        
        self._db_manager.modify("INSERT INTO logs (date, time, username, activity, additional_info, suspicious) VALUES (?, ?, ?, ?, ?, ?)",
                                (date, time, username, encrypted_description, encrypted_additional_info, suspicious))

    def flag_suspicious_activity(self, username, description):
        """
        Check if actiativity is suspicious
        """
        current_time = datetime.datetime.now()
        
        if description == "Unsuccessful login":
            self.failed_login_attempts[username] = self.failed_login_attempts.get(username, 0) + 1
            if self.failed_login_attempts[username] >= 3:
                return True
        
        elif description == "User deleted" or description == "Member deleted":
            self.recent_deletions.append(current_time)
            if len(self.recent_deletions) >= 3 and (self.recent_deletions[-1] - self.recent_deletions[-3]).seconds <= 300:
                return True
        
        elif description == "User role changed":
            self.recent_role_changes.append(current_time)
            if len(self.recent_role_changes) >= 2 and (self.recent_role_changes[-1] - self.recent_role_changes[-2]).seconds <= 300:
                return True
        
        elif description == "User logged in":
            if current_time.hour < 9 or current_time.hour > 18:
                return True
        
        # More conditions for other suspicious activities here
        
        return False

