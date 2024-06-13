from db import DBManager
from encryption import EncryptionManager
from mediator import EventHandler
import datetime

class Logger:
    _instance = None  

    @classmethod
    def get_instance(cls):
        """
        Singleton class to ensure only one instance of the Logger class is created.
        """
        if cls._instance is None:
            _EventHandler = EventHandler.get_instance()
            cls._instance = cls(_EventHandler)
        return cls._instance

    def __init__(self, event_handler):
        """
        Constructor for the Logger class.
        """
        if self._instance:
            raise Exception("You cannot create another Logger class!")
        
        self.failed_login_attempts = {}
        self.recent_deletions = []
        self.recent_role_changes = []
        self._db_manager = DBManager.get_instance()

        self._EncryptionManager = EncryptionManager(event_handler)

        self.event_handler = event_handler
        self.event_handler.register_listener("log_event", self.log_activity)

    def log_activity(self, data):
        """
        Log the activity to the database.
        """
        username, description, additional_info, *rest = data
        suspicious = rest[0] if rest else None

        date = str(datetime.date.today())
        time = str(datetime.datetime.now().time())[:8]
        
        encrypted_description = self._EncryptionManager.encrypt_data(description)
        encrypted_additional_info = self._EncryptionManager.encrypt_data(additional_info)

        if suspicious is None:
            suspicious = "Yes" if self.flag_suspicious_activity(username, description) else "No"
        
        self._db_manager.modify("INSERT INTO logs (date, time, username, activity, additional_info, suspicious, read) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (date, time, username, encrypted_description, encrypted_additional_info, suspicious, 'No'))

    def flag_suspicious_activity(self, username, description):
        """
        Check if activity is suspicious.
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
        
        return False

    def check_unread_suspicious_activities(self):
        """
        Check for unread suspicious activities.
        """
        print("Checking for unread suspicious activities...")
        suspicious_logs = self._db_manager.select_all("SELECT * FROM logs WHERE suspicious = 'Yes' AND read = 'No'", encrypt_indexes=[4, 5])
        if suspicious_logs:
            print("Unread suspicious activities detected:")
            for log in suspicious_logs:
                print(f"Date: {log[1]}, Time: {log[2]}, Username: {log[3]}, Activity: {log[4]}, Additional Info: {log[5]}")
            self._db_manager.modify("UPDATE logs SET read = 'Yes' WHERE suspicious = 'Yes' AND read = 'No'")
        else:
            print("No unread suspicious activities.")

