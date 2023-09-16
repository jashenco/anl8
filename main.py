from members import register_member
from db import DBManager

def main_menu():
    db = DBManager()
    db.create_tables()

    try:
        while True:
            print("1. Register New Member")
            print("2. Update Password")
            print("...")
            choice = input("Enter choice: ")
            if choice == "1":
                # Collect data from user
                # register_member(first_name, ...)
                pass
            elif choice == "2":
                pass

    except Exception as e:
        print("An error occurred: " + str(e))

main_menu()