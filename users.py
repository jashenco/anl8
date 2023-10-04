from db import DBManager
from encryption import decrypt_data
from logging import Logger

# TODO:
# - Make list of operations and permissions & implement in Authorization class
# - Rename db manager
# - Finish UserManager class
# - Implement Logger

class Authentication:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance:
            raise Exception("You cannot create another Authentication class!")
        self._DBManager = DBManager.get_instance()
        self._Logger = Logger.get_instance()
        self.current_user = None

    def login(self, username, password):
        user = self._DBManager.select("SELECT * FROM users WHERE username = ?", (username,))
        if user and decrypt_data(user[2]) == password:
            self._current_user = user
            self._Logger.log_activity(username, "User logged in", "")
            return True
        self._Logger.log_activity(username, "Unsuccessful login", "")
        return False

    def logout(self):
        self._current_user = None

    def is_authenticated(self):
        return self._current_user is not None

    def change_password(self, old_password, new_password):
        if self.is_authenticated() and decrypt_data(self._current_user[2]) == old_password:
            new_password = encrypt_data(new_password)
            self._DBManager.modify("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_password, self._current_user[0]))
            return True
        return False

class Authorization:
    _instance = None

    @classmethod
    def get_instance(cls, auth_instance):
        if cls._instance is None:
            cls._instance = cls(auth_instance)
        return cls._instance

    def __init__(self, auth_instance):
        if self._instance:
            raise Exception("You cannot create another Authorization class!")
        self.auth_instance = auth_instance

    def get_current_role(self):
        if self.auth_instance.is_authenticated():
            return self.auth_instance._current_user[3]
        return None

    def check_permission(self, action):
        role = self.get_current_role()
        # Example Check
        # IMPLEMENT DIFFERENT ACTIONS AND ROLES FROM FILE
        if role == "Super Administrator" and action == "get_list_of_users":
            return True
        return False

class UserManager:
    """
    Users are Admins (system and super) and Trainers
    """
    def __init__(self):
        self._DBManager = DBManager.get_instance()

    def create_user(self, username, password, role, first_name, last_name):
        pass

    def delete_user(self, user_id):
        pass

    def update_user(self, user_id, **kwargs):
        pass

    def get_list_of_users(self):
        print("List of Users and Roles:")
        pass