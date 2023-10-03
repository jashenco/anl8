from admin import delete_user, change_user_role, list_users, add_user, update_user, reset_password, update_own_password, logout_user, check_unread_suspicious_activities, read_logs, search_member, backup_system, restore_system
from authentication import login_user, get_current_role, get_current_username, logout_user
from members import register_member, get_member_details

# Dictionary to define the available options and their corresponding functions
menu_options = {
    '1': {
        'description': 'Check the list of users and their roles',
        'function': list_users
    },
    '2': {
        'description': 'Define and add a new trainer to the system',
        'function': add_user
    },
    '3': {
        'description': 'Modify or update an existing trainer’s account and profile',
        'function': update_user
    },
    # ... [Continue for all options]
}

def display_header():
    print("=======================================")
    print("            FitPlus System             ")
    print("=======================================")

def display_menu(role):
    display_header()
    print(f"\n{role} Menu:\n")
    for key, value in menu_options.items():
        print(f"{key}. {value['description']}")

    while True:
        choice = input("\nPlease enter the number corresponding to your choice: ")
        if choice in menu_options:
            menu_options[choice]['function']()
        else:
            print("Invalid choice. Please try again.")

# Main function to start the application
def main():
    global current_username, current_role

    display_header()
    print("\nWelcome to FitPlus! Please login to continue.\n")
    login_user()
    role = get_current_role()
    if role:
        display_menu(role)

if __name__ == "__main__":
    main()
