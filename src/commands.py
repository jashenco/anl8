from users import UserManager, Authorization, Authentication
from validation import InputValidator
from logging import Logger

_Authenticator = Authentication.get_instance()
_Authorizer = Authorization.get_instance(_Authenticator)

_UserManager = UserManager()
_Validator = InputValidator()
_Logger = Logger.get_instance()

# Commands have a common interface; execute and sometimes prompt for inputs
class Command:
    def get_validated_input(self, input_type, message):
        while True:
            user_input = input(message)
            validated_input = _Validator.validate(input_type, user_input)
            if validated_input is not False:
                return validated_input

    def execute(self):
        raise NotImplementedError("Subclasses must override this method")

class CheckListOfUsersCommand(Command):
    def execute(self):
        _UserManager.get_list_of_users()


class AddUserCommand(Command):
    def __init__(self, user_type):
        self.user_type = user_type

    def prompt_for_add_user(self):
        username = self.get_validated_input("username", "Enter the username for the new user: ")
        password = self.get_validated_input("password", "Enter a password for the new user: ")
        first_name = self.get_validated_input("name", "Enter the first name for the new user: ")
        last_name = self.get_validated_input("name", "Enter the last name for the new user: ")

        return username, password, self.user_type, first_name, last_name

    def execute(self):
        _UserManager.create_user(*self.prompt_for_add_user())

class UpdateUserCommand(Command):

    def prompt_for_update_user(self):
        user_id = self.get_validated_input("numeric", "Enter the user ID for the user to update: ")
        username = self.get_validated_input("username", "Enter the username for the user to update: ")
        password = self.get_validated_input("password", "Enter a new password for the user: ")
        role = self.get_validated_input("role", "Enter the new role for the user: ")
        first_name = self.get_validated_input("name", "Enter the new first name for the user: ")
        last_name = self.get_validated_input("name", "Enter the new last name for the user: ")

        return user_id, username, password, role, first_name, last_name

    def execute(self):
        _UserManager.update_user(*self.prompt_for_update_user())

class DeleteUserCommand(Command):
    def prompt_for_delete_user(self):
        user_id = self.get_validated_input("numeric", "Enter the user ID for the user to delete: ")
        return user_id

    def execute(self):
        _UserManager.delete_user(self.prompt_for_delete_user())

class UpdateUserPasswordCommand(Command):
    def prompt_for_update_user_password(self):
        user_id = self.get_validated_input("numeric", "Enter the user ID for the user to update: ")
        password = self.get_validated_input("password", "Enter a new password for the user: ")
        return user_id, password

    def execute(self):
        _UserManager.update_user_password(*self.prompt_for_update_user_password())


# MORE WORK NEEDED HERE
class BackupSystemCommand(Command):
    def execute(self):
        print("Backing up system...")
        # backup_system()

class ReadLogsCommand(Command):
    def execute(self):
        print("Reading logs...")
        # read_logs()

class RegisterMemberCommand(Command):
    def execute(self):
        print("Register member...")
        # register_member()

class GetMemberDetailsCommand(Command):
    def execute(self):
        print("Get member details...")
        # get_member_details()

class DeleteMemberCommand(Command):
    def execute(self):
        print("Delete member...")
        # delete_member()

class SearchMemberCommand(Command):
    def execute(self):
        print("Search member...")
        # search_member()

class UpdateMemberCommand(Command):
    def execute(self):
        print("Update member...")
        # update_member()

class ChangeUserRoleCommand(Command):
    def execute(self):
        print("Change user role...")
        # change_user_role()

class CheckUnreadSuspiciousActivitiesCommand(Command):
    def execute(self):
        print("Check unread suspicious activities...")
        # check_unread_suspicious_activities()

class RestoreSystemCommand(Command):
    def execute(self):
        print("Restore system...")
        # restore_system()

class LogoutCommand(Command):
    def execute(self):
        print("Logout...")
        # logout_user()

class UpdateOwnPasswordCommand(Command):
    def execute(self):
        print("Update own password...")
        # update_own_password()


# Register commands in the Factory
class CommandFactory:
    commands = {
        "list_users": CheckListOfUsersCommand(), 
        "add_trainer": AddUserCommand("Trainer"),
        "update_trainer": UpdateUserCommand(),
        "delete_trainer": DeleteUserCommand(),
        "reset_trainer_password": UpdateUserPasswordCommand(),
        "add_admin": AddUserCommand("System Administrator"),
        "update_admin": UpdateUserCommand(),
        "delete_admin": DeleteUserCommand(),
        "reset_admin_password": UpdateUserPasswordCommand(),
        "backup_system": BackupSystemCommand(),
        "read_logs": ReadLogsCommand(),
        "register_member": RegisterMemberCommand(),
        "get_member_details": GetMemberDetailsCommand(),
        "delete_member": DeleteMemberCommand(),
        "search_member": SearchMemberCommand(),
        "update_member": UpdateMemberCommand(),
        "change_user_role": ChangeUserRoleCommand(),
        "check_unread_suspicious_activities": CheckUnreadSuspiciousActivitiesCommand(),
        "restore_system": RestoreSystemCommand(),
        "logout": LogoutCommand(),
        "update_own_password": UpdateOwnPasswordCommand(),
    }

    @staticmethod
    def get_command(function_name):
        return CommandFactory.commands.get(function_name)
    
    def execute_function(self, function_name):
        try:
            command = self.get_command(function_name)
            if command:
                command.execute()
            else:
                print("Invalid command. Please try again.")
        except Exception as e:
            print("An unexpected error occurred while executing your command. Please try again.")
            _Logger.log_activity(_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "Exception occurred", str(e))


