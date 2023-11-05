from members import register_member, get_member_details
from users import UserManager
from validation import InputValidator

_UserManager = UserManager()
_Validator = InputValidator()

# Commands have a common interface; execute and sometimes prompt for inputs
class Command:
    def execute(self):
        raise NotImplementedError("Subclasses must override this method")

class CheckListOfUsersCommand(Command):
    def execute(self):
        _UserManager.check_list_of_users()

class AddTrainerCommand(Command):
    def prompt_for_add_user(self):
        username = _Validator.validate("username", input("Enter the username for the new user: "))
        password = _Validator.validate("password", input("Enter a password for the new user: "))
        first_name = _Validator.validate("name", input("Enter the first name for the new user: "))
        last_name = _Validator.validate("name", input("Enter the last name for the new user: "))

        if not username or not password or not first_name or not last_name:
            print("Invalid input. Try again.")
            return self.prompt_for_add_user()

        return username, password, "Trainer", first_name, last_name

    def execute(self):
        _UserManager.create_user(*self.prompt_for_add_user())

# Register commands in the Factory
class CommandFactory:
    commands = {
        "list_users": CheckListOfUsersCommand(), 
        "add_trainer": AddTrainerCommand(),
    }

    @staticmethod
    def get_command(function_name):
        return CommandFactory.commands.get(function_name)
    
    def execute_function(self, function_name):
        command = self.get_command(function_name)
        if command:
            command.execute()
        else:
            print("Invalid command")

""" Refactor this

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

"""


