from db import DBManager
from encryption import decrypt_data, encrypt_data
from logging import Logger
import bcrypt, json

# TODO:
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
        self._current_user = None

    def login(self, username, password):
        user = self._DBManager.select("SELECT * FROM users WHERE username = ?", (username,))
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
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
        if self.is_authenticated() and bcrypt.checkpw(old_password.encode('utf-8'), self._current_user[2].encode('utf-8')):
            new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self._DBManager.modify("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_hashed_password, self._current_user[0]))
            self._Logger.log_activity(self._current_user[1], "Password changed", "")
            return True
        self._Logger.log_activity(self._current_user[1], "Failed password change attempt", "")
        return False

class Authorization:
    _instance = None

    with open('permissions.json', 'r', encoding='utf-8') as file:
        role_permissions = json.load(file)

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
    
    def get_current_user(self):
        if self.auth_instance.is_authenticated():
            return self.auth_instance._current_user
        return None

    def check_permission(self, action):
        role = self.get_current_role()
        if role and action in self.role_permissions.get(role, {}):
            return True
        return False

    def get_role_options(self):
        role = self.get_current_role()
        return self.role_permissions.get(role, {})


class UserManager:
    def __init__(self):
        self._DBManager = DBManager.get_instance()
        self.ensure_super_admin()

    def hash_password(self, password):
        # Hash a password for the first time, with a randomly-generated salt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed

    def ensure_super_admin(self):
        # Check if the super admin exists, if not, create it
        super_admin = self._DBManager.select("SELECT * FROM users WHERE role = ?", ("Super Administrator",))
        if not super_admin:
            self.create_user("super_admin", "Admin_123!", "Super Administrator", "Super", "Admin")

    def create_user(self, username, password, role, first_name, last_name):
        hashed_password = self.hash_password(password)
        self._DBManager.modify("INSERT INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
                               (username, hashed_password, role, first_name, last_name))

    def delete_user(self, user_id):
        self._DBManager.modify("DELETE FROM users WHERE user_id = ?", (user_id,))

    def update_user(self, user_id, **kwargs):
        query = "UPDATE users SET "
        query += ", ".join([f"{key} = ?" for key in kwargs])
        query += " WHERE user_id = ?"
        self._DBManager.modify(query, (*kwargs.values(), user_id))

    def get_list_of_users(self):
        users = self._DBManager.select("SELECT user_id, username, role FROM users")
        for user in users:
            print(f"User ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")