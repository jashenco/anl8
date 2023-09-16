import sqlite3

def connect_db():
    try:
        conn = sqlite3.connect('fitplus.db')
        c = conn.cursor()
        return c, conn
    except Exception as e:
        print("An error occurred: " + str(e)) #Logging

def create_tables():
    try:
        c, conn = connect_db()

        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT, role TEXT, first_name TEXT, last_name TEXT, registration_date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS members
                    (member_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, weight REAL, address TEXT, email TEXT, phone TEXT, registration_date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                    (log_id INTEGER PRIMARY KEY, date TEXT, time TEXT, username TEXT, activity TEXT, additional_info TEXT, suspicious TEXT)''')
        
        conn.commit()
    except Exception as e:
        print("An error occurred: " + str(e)) #Logging
        
# Backups