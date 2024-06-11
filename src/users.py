from db import DBManager
from encryption import EncryptionManager
from logging import Logger
import bcrypt, json

from mediator import EventHandler

class Authentication:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self,):
        if self._instance:
            raise Exception("You cannot create another Authentication class!")
        self._DBManager = DBManager.get_instance()
        self._EventHandler = EventHandler.get_instance()
        self._EncryptionManager = EncryptionManager(self._EventHandler)
        self._current_user = None


    def login(self, username, password):
        print(username)
        user = self._DBManager.select("SELECT * FROM users WHERE username = ?", (username,))
        print(user)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            self._current_user = user
            self._EventHandler.emit("log_event", (username, "Login Successful", f"User {username} logged in"))
            return True
        self._EventHandler.emit("log_event", (username, "Unsuccessful login", f"Login attempt with username {username} failed."))
        return False


    def logout(self):
        self._current_user = None

    def is_authenticated(self):
        return self._current_user is not None

    def change_password(self, old_password, new_password):
        if self.is_authenticated() and bcrypt.checkpw(old_password.encode('utf-8'), self._current_user[2].encode('utf-8')):
            if self.validate_password(new_password):
                new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                self._DBManager.modify("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_hashed_password, self._current_user[0]))
                self._EventHandler.emit("log_event", (self._current_user[1], "Password changed", ""))
                return True
            else:
                print("New password does not meet complexity requirements.")
        self._EventHandler.emit("log_event", (self._current_user[1], "Failed password change attempt", ""))
        return False

    def validate_password(self, password):
        if (len(password) >= 12 and len(password) <= 30 and
            any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "~!@#$%&_-+=`|\\(){}[]:;'<>.?/" for c in password)):
            return True
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
            print('Authenticated')
            print(self.auth_instance._current_user)
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

_Authorizer = Authorization.get_instance(Authentication.get_instance())

class UserManager:
    def __init__(self):
        self._EventHandler = EventHandler.get_instance()
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
        if (username == 'super_admin' and password == 'Admin_123!') or (self.validate_password(password)):
            hashed_password = self.hash_password(password)
            self._DBManager.modify("INSERT INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
                                   (username, hashed_password, role, first_name, last_name),
                                   encrypt_indexes=[3, 4])
            self._EventHandler.emit("log_event", (username, "User created", f"User {username} created with role {role}."))
            print(f"User {username} created successfully.")
        else:
            print("Password does not meet complexity requirements.")

    def delete_user(self, user_id):
        self._DBManager.modify("DELETE FROM users WHERE user_id = ?", (user_id,))
        self._EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "User deleted", f"User ID {user_id} deleted."))
        print(f"User with ID {user_id} deleted successfully.")

    def update_user(self, user_id, username, password, role, first_name, last_name):
        if self.validate_password(password):
            hashed_password = self.hash_password(password)
            self._DBManager.modify("UPDATE users SET username = ?, password_hash = ?, role = ?, first_name = ?, last_name = ? WHERE user_id = ?",
                                   (username, hashed_password, role, first_name, last_name, user_id))
            self._EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "User updated", f"User ID: {user_id}"))
            print(f"User {username} updated successfully.")
        else:
            print("Password does not meet complexity requirements.")

    def update_user_password(self, user_id, password):
        if self.validate_password(password):
            hashed_password = self.hash_password(password)
            self._DBManager.modify("UPDATE users SET password_hash = ? WHERE user_id = ?",
                                   (hashed_password, user_id))
            self._EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "User password updated", f"User ID: {user_id}"))
            print(f"User password updated successfully.")
        else:
            print("Password does not meet complexity requirements.")

    def get_list_of_users(self):
        users = self._DBManager.select_all("SELECT user_id, username, role FROM users")
        for user in users:
            print(f"User ID: {str(user[0])}, Username: {user[1]}, Role: {user[2]}")

    def validate_password(self, password):
        if (len(password) >= 12 and len(password) <= 30 and
            any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "~!@#$%&_-+=`|\\(){}[]:;'<>.?/" for c in password)):
            return True
        return False