from authentication import login_user  # Assuming login_user is in a file named login.py
from admin import *  # Import all functions from admin.py
# Import other necessary modules and functions

# Global variables to hold the current user's username and role
current_username = None
current_role = None

def main_menu():
    global current_username, current_role
    
    while True:
        # Login
        current_username, current_role = login_user()
        
        # Main menu based on role
        if current_role == "Super Administrator":
            super_admin_menu()
        elif current_role == "System Administrator":
            system_admin_menu()
        elif current_role == "Trainer":
            trainer_menu()

def super_admin_menu():
    while True:
        print("\nSuper Administrator Menu:")
        print("1. Check the list of users and their roles")
        print("2. Define and add a new trainer to the system")
        print("3. Modify or update an existing trainer’s account and profile")
        print("4. Delete an existing trainer’s account")
        print("5. Reset an existing trainer’s password")
        print("6. Define and add a new admin to the system")
        print("7. Modify or update an existing admin’s account and profile")
        print("8. Delete an existing admin’s account")
        print("9. Reset an existing admin’s password")
        print("10. Make a backup of the system and restore a backup")
        print("11. See the logs file of the system")
        print("12. Add a new member to the system")
        print("13. Modify or update the information of a member in the system")
        print("14. Delete a member's record from the database")
        print("15. Search and retrieve the information of a member")
        print("16. Logout")
        
        choice = input("\nEnter the number of your choice and press enter: ")
        
        if choice == "1":
            list_users(current_role)
        # Add more elif conditions to call other functions
        elif choice == "16":
            logout()
            break

# Similar functions for system_admin_menu() and trainer_menu()

def logout():
    global current_username, current_role
    current_username = None
    current_role = None
    print("You have been logged out.")

if __name__ == "__main__":
    main_menu()
