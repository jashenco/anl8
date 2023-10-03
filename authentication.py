from db import connect_db
from logging import log_activity, flag_suspicious_activity
from encryption import decrypt_data

# Global variables to store the current user's username and role
current_username = None
current_role = None

def login_user():
    global current_username, current_role
    
    username = input("Enter username: ")
    password = input("Enter password: ")  # hash this
    
    c, conn = connect_db()
    
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    
    login_successful = False
    
    if user:
        decrypted_password = decrypt_data(user['password_hash'])
        if decrypted_password == password:  # replace with actual password hashing and verification logic
            login_successful = True
            current_username = username
            current_role = user['role']
    
    if login_successful:
        suspicious = flag_suspicious_activity(username, "User logged in")
        log_activity(username, "User logged in", "", suspicious)
        print(f"Welcome, {current_username}! You are logged in as {current_role}.")
    else:
        suspicious = flag_suspicious_activity(username, "Unsuccessful login")
        log_activity(username, "Unsuccessful login", "", suspicious)
        print("Login failed.")
    
    conn.close()
    return login_successful

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
