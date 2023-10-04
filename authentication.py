from db import DBManager
from logging import log_activity, flag_suspicious_activity
from encryption import decrypt_data

# Global variables to store the current user's username and role
current_username = None
current_role = None

_DBManager = DBManager()

def login_user():
    try:
        global current_username, current_role
        
        username = input("Enter username: ")
        password = input("Enter password: ")  # hash this
        
        user = _DBManager.select("SELECT * FROM users WHERE username = ?", (username,))

        print(type(user[2]), user[2])

        login_successful = False
        # Passwords are decrypted for verification. However, as per security best practices, 
        # passwords should ideally be hashed and then compared with the stored hash, rather than being decrypted.
        if user:
            print("decrypting password")
            decrypted_password = decrypt_data(user[2])
            print(decrypted_password)
            if decrypted_password == password:  # replace with actual password hashing and verification logic
                login_successful = True
                current_username = username
                current_role = user[3]
        
        if login_successful:
            suspicious = flag_suspicious_activity(username, "User logged in")
            log_activity(username, "User logged in", "", suspicious)
            print(f"Welcome, {current_username}! You are logged in as {current_role}.")
        else:
            suspicious = flag_suspicious_activity(username, "Unsuccessful login")
            log_activity(username, "Unsuccessful login", "", suspicious)
            print("Login failed.")

        return login_successful
    
    except Exception as e:
        print("An error occurred while logging in: " + str(e))

def get_current_role():
    global current_role
    return current_role

def get_current_username():
    global current_username
    return current_username

def logout_user():
    global current_username, current_role
    current_username = None
    current_role = None
    print("You have been logged out.")
