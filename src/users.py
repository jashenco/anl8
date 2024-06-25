from db import DBManager
from encryption import EncryptionManager
from logging import Logger
import bcrypt, json
import os
import time

from mediator import EventHandler

# Singleton class for Authentication
class Authentication:
    _instance = None

    @classmethod
    def get_instance(cls, db_manager=None, event_handler=None, encryption_manager=None, validator=None):
        if cls._instance is None:
            if db_manager is None or event_handler is None or encryption_manager is None:
                raise ValueError("Missing arguments for initializing Authentication")
            cls._instance = cls(db_manager, event_handler, encryption_manager, validator)
        return cls._instance

    def __init__(self, db_manager, event_handler, encryption_manager, validator):
        if self._instance:
            raise Exception("You cannot create another Authentication class!")
        self._DBManager = db_manager
        self._EventHandler = event_handler
        self._EncryptionManager = encryption_manager
        self._Validator = validator
        self._current_user = None
        self.failed_attempts = 0

    def login(self, username, password):
        """
        Log in a user with a username and password.
        """
        try:
            user = self._DBManager.select("SELECT * FROM users WHERE username = ?", (username,))
            if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
                self._current_user = user
                self.failed_attempts = 0  # Reset failed attempts on successful login
                self._EventHandler.emit("log_event", (username, "Login Successful", f"User {username} logged in"))
                return True
            else:
                self.failed_attempts += 1
                if self.failed_attempts >= 3:
                    time.sleep(5)  # Delay after 3 failed attempts
                self._EventHandler.emit("log_event", (username, "Unsuccessful login", "Invalid credentials"))
                return False
        except Exception as e:
            print(e)
            return False

    def logout(self):
        """
        Log out the current user.
        """
        self._current_user = None
        self._EventHandler.emit("log_event", ("System", "Logout", "User logged out"))
        return True

    def is_authenticated(self):
        """
        Check if a user is authenticated.
        """
        return self._current_user is not None

    def change_password(self, old_password, new_password):
        """
        Change the current user's password.
        """
        if self.is_authenticated() and bcrypt.checkpw(old_password.encode('utf-8'), self._current_user[2]):
            if self._Validator.validate("password", new_password):
                new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                self._DBManager.modify("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_hashed_password, self._current_user[0]))
                self._EventHandler.emit("log_event", (self._current_user[1], "Password changed", ""))
                return True
            else:
                print("New password does not meet complexity requirements.")
        self._EventHandler.emit("log_event", (self._current_user[1], "Failed password change attempt", ""))
        return False
    
# Singleton class for Authorization
class Authorization:
    _instance = None

    # Get the absolute path of the directory of the script
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Change the working directory
    os.chdir(dir_path)

    # Now you can open the file with just its name
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
        """
        Get the current user's role.
        """
        if self.auth_instance.is_authenticated():
            return self.auth_instance._current_user[3]
        return None
    
    def get_current_user(self):
        """
        Get the current user.
        """
        if self.auth_instance.is_authenticated():
            return self.auth_instance._current_user
        return None

    def check_permission(self, action):
        """
        Check if the current user has permission for a specific action.
        """
        role = self.get_current_role()
        if role and action in self.role_permissions.get(role, {}):
            return True
        return False

    def get_role_options(self):
        """
        Get the available options for the current user's role.
        """
        role = self.get_current_role()
        return self.role_permissions.get(role, {})

# Class to manage users
class UserManager:
    def __init__(self, event_handler, db_manager, validator):
        self._EventHandler = event_handler
        self._DBManager = db_manager
        self._Validator = validator
        self.ensure_super_admin()

    def hash_password(self, password):
        """
        Hash a password for storage.
        """
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed

    def ensure_super_admin(self):
        """
        Ensure the super admin account exists.
        """
        super_admin = self._DBManager.select(
            "SELECT * FROM users WHERE role = ?", 
            ("Super Administrator",),
            encrypt_indexes=[4, 5]
        )
        if not super_admin:
            self.create_user("super_admin", "Admin_123!", "Super Administrator", "Super", "Admin")

    def create_user(self, username, password, role, first_name, last_name):
        """
        Create a new user account.
        """
        if (username == 'super_admin' and password == 'Admin_123!') or (self._Validator.validate("password", password)):
            hashed_password = self.hash_password(password)
            self._DBManager.modify("INSERT INTO users (username, password_hash, role, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
                                   (username, hashed_password, role, first_name, last_name),
                                   encrypt_indexes=[3, 4])
            self._EventHandler.emit("log_event", (username, "User created", f"User {username} created with role {role}."))
            print(f"User {username} created successfully.")
        else:
            print("Password does not meet complexity requirements.")

    def delete_user(self, user_id):
        """
        Delete a user account.
        """
        self._DBManager.modify("DELETE FROM users WHERE user_id = ?", (user_id,))
        self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._EventHandler.get_current_user() else "System", "User deleted", f"User ID {user_id} deleted."))
        print(f"User with ID {user_id} deleted successfully.")

    def update_user(self, user_id, username, password, role, first_name, last_name):
        """
        Update an existing user's account information.
        """
        if self._Validator.validate("password", password):
            hashed_password = self.hash_password(password)
            self._DBManager.modify("UPDATE users SET username = ?, password_hash = ?, role = ?, first_name = ?, last_name = ? WHERE user_id = ?",
                                   (username, hashed_password, role, first_name, last_name, user_id),
                                   encrypt_indexes=[3, 4])
            self._EventHandler.emit("log_event", (self._EventHandler.get_current_user()[1] if self._EventHandler.get_current_user() else "System", "User updated", f"User ID: {user_id}"))
            print(f"User {username} updated successfully.")
        else:
            print("Password does not meet complexity requirements.")

    def update_user_password(self, user_id, password):
        """
        Update a user's password.
        """
        if self._Validator.validate("password", password):
            hashed_password = self.hash_password(password)
            self._DBManager.modify("UPDATE users SET password_hash = ? WHERE user_id = ?",
                                   (hashed_password, user_id))
            self._EventHandler.emit("log_event", (self._EventHandler.get_current_user()[1] if self._EventHandler.get_current_user() else "System", "User password updated", f"User ID: {user_id}"))
            print(f"User password updated successfully.")
        else:
            print("Password does not meet complexity requirements.")

    def get_list_of_users(self):
        """
        Get and display a list of all users.
        """
        users = self._DBManager.select_all("SELECT user_id, username, role FROM users")
        for user in users:
            print(f"User ID: {str(user[0])}, Username: {user[1]}, Role: {user[2]}")
