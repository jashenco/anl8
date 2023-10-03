from db import connect_db
from encryption import encrypt_data
from datetime import datetime

# Global variable
failed_login_attempts = {}
recent_deletions = []
recent_role_changes = []

def log_activity(username, description, additional_info, suspicious):
    c, conn = connect_db()
    
    date = str(datetime.date.today())
    time = str(datetime.datetime.now().time())[:8]  # HH:MM:SS format
    
    encrypted_description = encrypt_data(description)
    encrypted_additional_info = encrypt_data(additional_info)
    
    c.execute("INSERT INTO logs (date, time, username, activity, additional_info, suspicious) VALUES (?, ?, ?, ?, ?, ?)",
              (date, time, username, encrypted_description, encrypted_additional_info, suspicious))
    
    conn.commit()
    conn.close()

def flag_suspicious_activity(username, description):
    global failed_login_attempts, recent_deletions, recent_role_changes
    
    suspicious = "No"
    current_time = datetime.now()
    
    if description == "Unsuccessful login":
        failed_login_attempts[username] = failed_login_attempts.get(username, 0) + 1
        if failed_login_attempts[username] >= 3:
            suspicious = "Yes"
    
    elif description == "User deleted" or description == "Member deleted":
        recent_deletions.append(current_time)
        if len(recent_deletions) >= 3 and (recent_deletions[-1] - recent_deletions[-3]).seconds <= 300:
            suspicious = "Yes"
    
    elif description == "User role changed":
        recent_role_changes.append(current_time)
        if len(recent_role_changes) >= 2 and (recent_role_changes[-1] - recent_role_changes[-2]).seconds <= 300:
            suspicious = "Yes"
    
    elif description == "User logged in":
        if current_time.hour < 9 or current_time.hour > 18:
            suspicious = "Yes"
    
    # More conditions for other suspicious activities here
    
    return suspicious

