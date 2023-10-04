# Integrating everything into a cohesive piece of code

# Assuming the following imports based on the provided files and functionalities
from admin import delete_user, change_user_role, list_users, add_user, update_user, reset_password, update_own_password, logout_user, check_unread_suspicious_activities, read_logs, search_member, backup_system, restore_system
from authentication import login_user, get_current_role, get_current_username, logout_user
from members import register_member, get_member_details
from db import *

# Global variable to hold the current user's role after successful login
current_role = None

# Defining the role-specific menu options based on the functions and their descriptions
# move this to a seperate file for readability
super_admin_options = {
    '1': {'description': 'Check the list of users and their roles', 'function': 'list_users'},
    '2': {'description': 'Define and add a new trainer to the system', 'function': 'add_user'},
    '3': {'description': 'Modify or update an existing trainer’s account and profile', 'function': 'update_user'},
    '4': {'description': 'Delete an existing trainer’s account', 'function': 'delete_user'},
    '5': {'description': 'Reset an existing trainer’s password', 'function': 'reset_password'},
    '6': {'description': 'Define and add a new admin to the system', 'function': 'add_user'},
    '7': {'description': 'Modify or update an existing admin’s account and profile', 'function': 'update_user'},
    '8': {'description': 'Delete an existing admin’s account', 'function': 'delete_user'},
    '9': {'description': 'Reset an existing admin’s password', 'function': 'reset_password'},
    '10': {'description': 'Make a backup of the system and restore a backup', 'function': 'backup_system'},
    '11': {'description': 'See the logs file of the system', 'function': 'read_logs'},
    '12': {'description': 'Add a new member to the system', 'function': 'register_member'},
    '13': {'description': 'Modify or update the information of a member in the system', 'function': 'get_member_details'},
    '14': {'description': 'Delete a member\'s record from the database', 'function': 'delete_member'},  # Assuming the function name
    '15': {'description': 'Search and retrieve the information of a member', 'function': 'search_member'},
    '16': {'description': 'Change user role', 'function': 'change_user_role'},
    '17': {'description': 'Check unread suspicious activities', 'function': 'check_unread_suspicious_activities'},
    '18': {'description': 'Restore system from a backup', 'function': 'restore_system'},
    '19': {'description': 'List all users', 'function': 'list_users'},
    '20': {'description': 'Logout', 'function': 'logout_user'}
}

system_admin_options = {
    '1': {'description': 'Update their own password', 'function': 'update_own_password'},
    '2': {'description': 'Check the list of users and their roles', 'function': 'list_users'},
    '3': {'description': 'Define and add a new trainer to the system', 'function': 'add_user'},
    '4': {'description': 'Modify or update an existing trainer’s account and profile', 'function': 'update_user'},
    '5': {'description': 'Delete an existing trainer’s account', 'function': 'delete_user'},
    '6': {'description': 'Reset an existing trainer’s password', 'function': 'reset_password'},
    '7': {'description': 'Make a backup of the system and restore a backup', 'function': 'backup_system'},
    '8': {'description': 'See the logs file(s) of the system', 'function': 'read_logs'},
    '9': {'description': 'Add a new member to the system', 'function': 'register_member'},
    '10': {'description': 'Modify or update the information of a member in the system', 'function': 'get_member_details'},
    '11': {'description': 'Delete a member\'s record from the database', 'function': 'delete_member'},  # Assuming the function name
    '12': {'description': 'Search and retrieve the information of a member', 'function': 'search_member'},
    '13': {'description': 'Check unread suspicious activities', 'function': 'check_unread_suspicious_activities'},
    '14': {'description': 'Restore system from a backup', 'function': 'restore_system'},
    '15': {'description': 'List all users', 'function': 'list_users'},
    '16': {'description': 'Logout', 'function': 'logout_user'}
}

trainer_options = {
    '1': {'description': 'Update their own password', 'function': 'update_own_password'},
    '2': {'description': 'Add a new member to the system', 'function': 'register_member'},
    '3': {'description': 'Modify or update the information of a member in the system', 'function': 'get_member_details'},
    '4': {'description': 'Search and retrieve the information of a member', 'function': 'search_member'},
    '5': {'description': 'Logout', 'function': 'logout_user'}
}


# Function to integrate actual functions and gather inputs
def execute_function(function_name):
    if function_name == "register_member":
        prompt_for_member_registration()
    elif function_name == "get_member_details":
        prompt_for_member_details()
    elif function_name == "add_user":
        prompt_for_add_user()
    elif function_name == "update_user":
        prompt_for_update_user()
    elif function_name == "reset_password":
        prompt_for_reset_password()
    elif function_name == "update_own_password":
        prompt_for_update_own_password()
    elif function_name == "logout_user":
        logout_user()
    elif function_name == "change_user_role":
        prompt_for_change_user_role()
    elif function_name == "check_unread_suspicious_activities":
        check_unread_suspicious_activities()
    elif function_name == "restore_system":
        prompt_for_restore_system()
    elif function_name == "list_users":
        list_users()
    else:
        print(f"Executing {function_name}...")

# Role-specific menu options with integrated functions and their input prompts
def prompt_for_member_registration():
    first_name = input("Enter member's first name: ")
    last_name = input("Enter member's last name: ")
    age = input("Enter member's age: ")
    gender = input("Enter member's gender (M/F): ")
    weight = input("Enter member's weight (in kg): ")
    address = input("Enter member's address: ")
    email = input("Enter member's email address: ")
    phone = input("Enter member's phone number: ")
    register_member(first_name, last_name, age, gender, weight, address, email, phone)

def prompt_for_member_details():
    member_id = input("Enter the member ID to retrieve details: ")
    get_member_details(member_id)

def prompt_for_add_user():
    username = input("Enter the username for the new user: ")
    password = input("Enter a password for the new user: ")
    role = input("Enter the role for the new user (Trainer, System Administrator, Super Administrator): ")
    add_user(username, password, role, current_role)

def prompt_for_update_user():
    username = input("Enter the username of the user you want to update: ")
    new_details = input("Enter the new details for the user (in a format you define, e.g., 'new_username,new_password,new_role'): ")
    update_user(username, new_details, current_role)

def prompt_for_delete_user():
    username_to_delete = input("Enter the username of the user you want to delete: ")
    delete_user(username_to_delete, current_role)

def prompt_for_reset_password():
    username = input("Enter the username of the user whose password you want to reset: ")
    new_password = input("Enter the new password for the user: ")
    reset_password(username, new_password, current_role)

def prompt_for_update_own_password():
    new_password = input("Enter your new password: ")
    update_own_password(get_current_username(), new_password, current_role)

def prompt_for_backup_system():
    # Assuming no input is needed, the function directly backs up the system
    backup_system(current_role)

def prompt_for_search_member():
    member_id = input("Enter the ID of the member you want to search for: ")
    search_member(member_id, current_role)

def prompt_for_change_user_role():
    username = input("Enter the username whose role you want to change: ")
    new_role = input("Enter the new role for the user (Super Administrator/System Administrator/Trainer): ")
    change_user_role(username, new_role)

def prompt_for_restore_system():
    confirm = input("Are you sure you want to restore the system from a backup? (yes/no): ")
    if confirm.lower() == 'yes':
        restore_system()

# Updated the display_menu function to show role-specific options and gather inputs
def display_menu():
    global current_role
    display_header()
    print(f"\n{current_role} Menu:\n")
    
    options = {
        'Super Administrator': super_admin_options,
        'System Administrator': system_admin_options,
        'Trainer': trainer_options
    }
    
    for key, value in options[current_role].items():
        print(f"{key}. {value['description']}")
    
    while True:
        choice = input("\nPlease enter the number corresponding to your choice (or 'exit' to exit): ")
        if choice == "exit":
            break
        if choice in options[current_role]:
            function_name = options[current_role][choice]['function']
            execute_function(function_name)
        else:
            print("Invalid choice. Please try again.")

def display_header():
    print("=======================================")
    print("            FitPlus System             ")
    print("=======================================")

# Main function to start the application
def main():
    global current_role
    display_header()
    print("\nWelcome to FitPlus! Please login to continue.\n")
    login_user()
    current_role = get_current_role()
    if current_role:
        display_menu()

connect_db()
create_tables()
main()

if __name__ == "__main__":
    main()
