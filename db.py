import sqlite3

from encryption import encrypt_data

def connect_db():
    try:
        conn = sqlite3.connect('fitplus.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        return c, conn
    except Exception as e:
        print("An error occurred during DB connection: " + str(e))

def create_tables():
    try:
        c, conn = connect_db()

        # Create users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password_hash TEXT, role TEXT, first_name TEXT, last_name TEXT, registration_date TEXT)''')
        print("Users table created successfully.")
        conn.commit()

        # Create members table
        c.execute('''CREATE TABLE IF NOT EXISTS members
                    (member_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, weight REAL, address TEXT, email TEXT, phone TEXT, registration_date TEXT)''')
        print("Members table created successfully.")
        conn.commit()

        # Create logs table
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                    (log_id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, username TEXT, activity TEXT, additional_info TEXT, suspicious TEXT)''')
        print("Logs table created successfully.")
        conn.commit()
        
        # Placeholder Super Admin's credentials
        username = "SuperAdmin2"
        passwordnormal = "password12"
        password = encrypt_data(passwordnormal)

        # Insert the Super Admin's credentials into the users table
        try:
            c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                   (username, password, "Super Administrator"))
            conn.commit()
            print("Super Admin seeded successfully.")
        except sqlite3.IntegrityError:
            print("Super Admin is already in the database.")
            pass

    except Exception as e:
        print("An error occurred during table creation or seeding: " + str(e))

# Display SQLite version for debugging
def check_sqlite_version():
    c, conn = connect_db()
    version = c.execute("SELECT sqlite_version()").fetchone()
    print("SQLite version:", version[0])
    conn.close()

# Call this at the start to check SQLite version
check_sqlite_version()

# Call create_tables function to setup DB
create_tables()