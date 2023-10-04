from db import DBManager
from encryption import decrypt_data, encrypt_data
from logging import log_activity, flag_suspicious_activity

_DBManager = DBManager()

# Function to delete a user
def delete_user(username_to_delete, current_role):
    if current_role not in ['Super Administrator', 'System Administrator']:
        print("Unauthorized access.")
        return
    
    _DBManager.modify("DELETE FROM users WHERE username = ?", (username_to_delete,))
    
    suspicious = flag_suspicious_activity("system", "User deleted")
    log_activity("system", "User deleted", f"Deleted username: {username_to_delete}", suspicious)

def change_user_role(username, new_role):
    _DBManager.modify("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
    
    suspicious = flag_suspicious_activity("system", "User role changed")
    log_activity("system", "User role changed", f"Changed role for {username} to {new_role}", suspicious)

# Function to check the list of users and their roles
def list_users(current_role):
    if current_role not in ["Super Administrator", "System Administrator"]:
        print("You do not have permission to perform this action.")
        return

    rows = _DBManager.select_all("SELECT username, role FROM users")
    
    print("List of Users and Roles:")
    for row in rows:
        print(f"{row['username']} - {row['role']}")
    # add flagging/logging

# Function to add a new trainer/admin
def add_user(username, password, role, current_role):
    if current_role != "Super Administrator":
        print("You do not have permission to perform this action.")
        return
    
    encrypted_password = encrypt_data(password)
    _DBManager.modify("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (username, encrypted_password, role))
    
    suspicious = flag_suspicious_activity("system", "User added")
    log_activity("system", "User added", f"Added username: {username}, role: {role}", suspicious)

# Function to update user details
def update_user(username, new_details, current_role):
    if current_role != "Super Administrator":
        print("You do not have permission to perform this action.")
        return
    
    # Assuming new_details is a dictionary with keys matching the column names
    for key, value in new_details.items():
        _DBManager.modify(f"UPDATE users SET {key} = ? WHERE username = ?", (value, username))
    
    suspicious = flag_suspicious_activity("system", "User updated")
    log_activity("system", "User updated", f"Updated username: {username}", suspicious)

# Function to reset user password
def reset_password(username, new_password, current_role):
    if current_role not in ["Super Administrator", "System Administrator"]:
        print("You do not have permission to perform this action.")
        return
    
    encrypted_new_password = encrypt_data(new_password)
    _DBManager.modify("UPDATE users SET password_hash = ? WHERE username = ?", (encrypted_new_password, username))
    
    suspicious = flag_suspicious_activity("system", "Password reset")
    log_activity("system", "Password reset", f"Reset password for username: {username}", suspicious)


# Update Own Password
def update_own_password(username, new_password, current_role):
    if current_role not in ["System Administrator", "Trainer"]:
        print("You do not have permission to perform this action.")
        return
    
    encrypted_new_password = encrypt_data(new_password)
    _DBManager.modify("UPDATE users SET password_hash = ? WHERE username = ?", (encrypted_new_password, username))
    
    suspicious = flag_suspicious_activity("system", "Password updated")
    log_activity("system", "Password updated", f"Updated password for username: {username}", suspicious)

# Logout Function
def logout_user(username, current_role):
    # Invalidate session or token here
    
    suspicious = flag_suspicious_activity("system", "User logout")
    log_activity("system", "User logout", f"User {username} with role {current_role} logged out", suspicious)

def check_unread_suspicious_activities():    
    rows = _DBManager.select_all("SELECT * FROM logs WHERE suspicious = 'Yes'")
    
    for row in rows:
        decrypted_activity = decrypt_data(row['activity'])
        print(f"Alert: Suspicious activity detected - {decrypted_activity}")
        # add flagging/logging

def read_logs():   
    rows = _DBManager.select_all("SELECT * FROM logs")
    
    for row in rows:
        decrypted_activity = decrypt_data(row['activity'])
        decrypted_additional_info = decrypt_data(row['additional_info'])
        print(f"{row['date']} {row['time']} {row['username']} {decrypted_activity} {decrypted_additional_info} {row['suspicious']}")
    # add flagging/logging

# Search and Retrieve Member Information
def search_member(member_id, current_role):
    if current_role not in ["Super Administrator", "System Administrator", "Trainer"]:
        print("You do not have permission to perform this action.")
        return

    row = _DBManager.select("SELECT * FROM members WHERE member_id = ?", (member_id,))
    
    if row:
        print(f"Member ID: {row['member_id']}, Name: {row['first_name']} {row['last_name']}")
    else:
        print("Member not found.")

# Implementing Encrypted Backup and Restore Logic
def backup_system(current_role):
    if current_role != "Super Administrator":
        print("You do not have permission to perform this action.")
        return
    
    # let's assume we're backing up to a file named 'encrypted_backup.txt'
    rows = _DBManager.select_all("SELECT * FROM members")
    
    with open('encrypted_backup.txt', 'w') as f:
        for row in rows:
            encrypted_row = encrypt_data(str(row))
            f.write(encrypted_row + '\n')
    
    suspicious = flag_suspicious_activity("system", "System backup")
    log_activity("system", "System backup", "Encrypted backup created", suspicious)

def restore_system(current_role):
    if current_role != "Super Administrator":
        print("You do not have permission to perform this action.")
        return
    
    # let's assume we're restoring from a file named 'encrypted_backup.txt'
    with open('encrypted_backup.txt', 'r') as f:
        for line in f:
            decrypted_line = decrypt_data(line.strip())
            row = eval(decrypted_line)
            _DBManager.modify("INSERT INTO members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
    
    suspicious = flag_suspicious_activity("system", "System restore")
    log_activity("system", "System restore", "Encrypted backup restored", suspicious)