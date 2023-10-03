from db import connect_db
from encryption import decrypt_data

# run 'python -m unittest discover -s tests' to run all tests at once :)

def activity_logged(username, description):
    c, conn = connect_db()
    c.execute("SELECT * FROM logs WHERE username = ?", (username,))
    activities = c.fetchall()
    conn.close()
    
    for activity in activities:
        if decrypt_data(activity['activity']) == description:
            return True
    return False

def user_exists(username):
    c, conn = connect_db()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return bool(user)

def get_user_role(username):
    c, conn = connect_db()
    c.execute("SELECT role FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user['role'] if user else None

