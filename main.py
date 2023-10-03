from authentication import login_user  # Assuming login_user is in a file named login.py
from admin import *  # Import all functions from admin.py
from members import *
# Import other necessary modules and functions

# Global variables to hold the current user's username and role
current_username = None
current_role = None

def display_header():
    print("=======================================")
    print("            FitPlus System             ")
    print("=======================================")

def main_menu():
    global current_username, current_role
    
    display_header()
    print("\nWelcome to FitPlus! Please login to continue.\n")
    
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
    def display_header():
        print("\n" + "="*30)
        print("FitPlus - Super Administrator Menu")
        print("="*30)

    def list_users_option():
        list_users("Super Administrator")

    def add_trainer_option(): #todo: add the sanitized_input to all user inputs in options. 
        username = sanitized_input("Enter the new trainer's username (alphanumeric and underscores only): ", valid_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        password = input("Enter the new trainer's password: ")
        add_user(username, password, "Trainer", "Super Administrator")

    def update_trainer_option():
        username = input("Enter the trainer's username to update: ")
        new_details = input("Enter the new details for the trainer: ")  # This can be further broken down based on what details you want to update
        update_user(username, new_details, "Super Administrator")

    def delete_trainer_option():
        username = input("Enter the trainer's username to delete: ")
        delete_user(username, "Super Administrator")

    def reset_trainer_password_option():
        username = input("Enter the trainer's username to reset password: ")
        new_password = input("Enter the new password for the trainer: ")
        reset_password(username, new_password, "Super Administrator")

    def add_admin_option():
        username = input("Enter the new admin's username: ")
        password = input("Enter the new admin's password: ")
        add_user(username, password, "Admin", "Super Administrator")

    def update_admin_option():
        username = input("Enter the admin's username to update: ")
        new_details = input("Enter the new details for the admin: ")
        update_user(username, new_details, "Super Administrator")

    def delete_admin_option():
        username = input("Enter the admin's username to delete: ")
        delete_user(username, "Super Administrator")

    def reset_admin_password_option():
        username = input("Enter the admin's username to reset password: ")
        new_password = input("Enter the new password for the admin: ")
        reset_password(username, new_password, "Super Administrator")

    def backup_system_option():
        backup_system("Super Administrator")

    def restore_system_option():
        restore_system("Super Administrator")

    def view_logs_option():
        read_logs()

    def add_member_option():
        # Assuming member details include first name, last name, etc.
        first_name = input("Enter the new member's first name: ")
        last_name = input("Enter the new member's last name: ")
        # ... (collect other details)
        add_member(first_name, last_name, ... , "Super Administrator")

    def update_member_option():
        member_id = input("Enter the member's ID to update: ")
        new_details = input("Enter the new details for the member: ")
        update_member(member_id, new_details, "Super Administrator")

    def delete_member_option():
        member_id = input("Enter the member's ID to delete: ")
        delete_member(member_id, "Super Administrator")

    def search_member_option():
        search_query = input("Enter the search query for the member: ")
        search_member(search_query)

    options = {
        "1": list_users_option,
        "2": add_trainer_option,
        "3": update_trainer_option,
        "4": delete_trainer_option,
        "5": reset_trainer_password_option,
        "6": add_admin_option,
        "7": update_admin_option,
        "8": delete_admin_option,
        "9": reset_admin_password_option,
        "10": backup_system_option,
        "11": restore_system_option,
        "12": view_logs_option,
        "13": add_member_option,
        "14": update_member_option,
        "15": delete_member_option,
        "16": search_member_option,
    }

    while True:
        display_header()
        print("\n1. Check the list of users and their roles")
        print("2. Define and add a new trainer to the system")
        print("3. Modify or update an existing trainer’s account and profile")
        print("4. Delete an existing trainer’s account")
        print("5. Reset an existing trainer’s password")
        print("6. Define and add a new admin to the system")
        print("7. Modify or update an existing admin’s account and profile")
        print("8. Delete an existing admin’s account")
        print("9. Reset an existing admin’s password")
        print("10. Make a backup of the system")
        print("11. Restore a backup")
        print("12. See the logs file of the system")
        print("13. Add a new member to the system")
        print("14. Modify or update the information of a member in the system")
        print("15. Delete a member's record from the database")
        print("16. Search and retrieve the information of a member")
        print("17. Logout")

        choice = input("\nEnter the number of your choice (1-17): ")

        if choice in options:
            options[choice]()
        elif choice == "17":
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 17.")


# Similar functions for system_admin_menu() and trainer_menu()

def logout():
    global current_username, current_role
    current_username = None
    current_role = None
    print("\nYou have been logged out. Thank you for using FitPlus!\n")

# Input validation for options
def sanitized_input(prompt, valid_chars=None):
    """
    Get input from the user and sanitize it.
    If valid_chars is provided, only those characters are allowed in the input.
    """
    while True:
        user_input = input(prompt)
        if valid_chars:
            if all(char in valid_chars for char in user_input):
                return user_input
            else:
                print("Invalid input. Please try again.")
        else:
            return user_input


if __name__ == "__main__":
    main_menu()
