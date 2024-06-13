import datetime
import random
import shutil
import os
import zipfile
from users import UserManager, Authorization, Authentication
from validation import InputValidator
from logging import Logger
from db import DBManager

_Authenticator = Authentication.get_instance()
_Authorizer = Authorization.get_instance(_Authenticator)

_UserManager = UserManager()
_Validator = InputValidator()
_Logger = Logger.get_instance()
_DBManager = DBManager.get_instance()

# Commands have a common interface; execute and sometimes prompt for inputs
class Command:     
    def get_validated_input(self, input_type, message):
        """
        Prompt the user for input and validate it based on the input type.
        """
        while True:
            user_input = input(message)
            validated_input = _Validator.validate(input_type, user_input)
            if validated_input is not False:
                return validated_input

    def execute(self):
        """
        Execute the command. Must be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must override this method")

class CheckListOfUsersCommand(Command):
    def execute(self):
        """
        Execute the command to list all users.
        """
        _UserManager.get_list_of_users()
        _Logger.log_activity((_Authorizer.get_current_user()[1], "Checked list of users", ""))

class AddUserCommand(Command):
    def __init__(self, user_type):
        """
        Initialize the command with the type of user to add.
        """
        self.user_type = user_type

    def prompt_for_add_user(self):
        """
        Prompt for the necessary information to add a new user.
        """
        username = self.get_validated_input("username", "Enter the username for the new user: ")
        password = self.get_validated_input("password", "Enter a password for the new user: ")
        first_name = self.get_validated_input("name", "Enter the first name for the new user: ")
        last_name = self.get_validated_input("name", "Enter the last name for the new user: ")

        return username, password, self.user_type, first_name, last_name

    def execute(self):
        """
        Execute the command to add a new user.
        """
        _UserManager.create_user(*self.prompt_for_add_user())
        _Logger.log_activity((_Authorizer.get_current_user()[1], "Added new user", f"User type: {self.user_type}"))

class UpdateUserCommand(Command):
    def prompt_for_update_user(self):
        """
        Prompt for the necessary information to update a user.
        """
        user_id = self.get_validated_input("numeric", "Enter the user ID for the user to update: ")
        username = self.get_validated_input("username", "Enter the username for the user to update: ")
        password = self.get_validated_input("password", "Enter a new password for the user: ")
        role = self.get_validated_input("role", "Enter the new role for the user: ")
        first_name = self.get_validated_input("name", "Enter the new first name for the user: ")
        last_name = self.get_validated_input("name", "Enter the new last name for the user: ")

        return user_id, username, password, role, first_name, last_name

    def execute(self):
        """
        Execute the command to update a user.
        """
        _UserManager.update_user(*self.prompt_for_update_user())
        _Logger.log_activity((_Authorizer.get_current_user()[1], "Updated user", ""))

class DeleteUserCommand(Command):
    def prompt_for_delete_user(self):
        """
        Prompt for the user ID to delete.
        """
        user_id = self.get_validated_input("numeric", "Enter the user ID for the user to delete: ")
        return user_id

    def execute(self):
        """
        Execute the command to delete a user.
        """
        _UserManager.delete_user(self.prompt_for_delete_user())
        _Logger.log_activity((_Authorizer.get_current_user()[1], "Deleted user", ""))

class UpdateUserPasswordCommand(Command):
    def prompt_for_update_user_password(self):
        """
        Prompt for the necessary information to update a user's password.
        """
        user_id = self.get_validated_input("numeric", "Enter the user ID for the user to update: ")
        password = self.get_validated_input("password", "Enter a new password for the user: ")
        return user_id, password

    def execute(self):
        """
        Execute the command to update a user's password.
        """
        _UserManager.update_user_password(*self.prompt_for_update_user_password())
        _Logger.log_activity((_Authorizer.get_current_user()[1], "Updated user password", ""))

class BackupSystemCommand(Command):
    def execute(self):
        """
        Execute the command to backup the system.
        """
        try:
            # Backup the database file
            shutil.copyfile('uniquemeal.db', 'backup_uniquemeal.db')

            # Backup the log file
            # shutil.copyfile('logs.db', 'backup_logs.db')

            # Create a zip file containing the backup files
            with zipfile.ZipFile('backup.zip', 'w') as backup_zip:
                backup_zip.write('backup_uniquemeal.db')
                # backup_zip.write('backup_logs.db')

            # Remove the temporary backup files
            os.remove('backup_uniquemeal.db')
            # os.remove('backup_logs.db')

            _Logger.log_activity((_Authorizer.get_current_user()[1], "Backup system", ""))
            print("System backed up successfully.")
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Backup system failed", str(e)))
            print("Failed to backup system.")

class ReadLogsCommand(Command):
    def execute(self):
        """
        Execute the command to read system logs.
        """
        try:
            logs = _DBManager.select_all("SELECT * FROM logs", encrypt_indexes=[4, 5])
            for log in logs:
                print(log)
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Read logs", ""))
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Read logs failed", str(e)))
            print("Failed to read logs.")

class RegisterMemberCommand(Command):
    def execute(self):
        """
        Execute the command to register a new member.
        """
        try:
            first_name = self.get_validated_input("name", "Enter the first name of the member: ")
            last_name = self.get_validated_input("name", "Enter the last name of the member: ")
            age = self.get_validated_input("numeric", "Enter the age of the member: ")
            gender = self.get_validated_input("alpha", "Enter the gender of the member: ")
            weight = self.get_validated_input("numeric", "Enter the weight of the member: ")
            address = input("Enter the address of the member: ")
            email = self.get_validated_input("email", "Enter the email of the member: ")
            phone = self.get_validated_input("phone", "Enter the phone number of the member: ")

            member_id = self.generate_member_id()
            registration_date = str(datetime.date.today())

            _DBManager.modify(
                "INSERT INTO members (member_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (member_id, first_name, last_name, age, gender, weight, address, email, phone, registration_date),
                encrypt_indexes=[1, 2, 3, 4, 5, 6, 7, 8, 9]
            )

            _Logger.log_activity((_Authorizer.get_current_user()[1], "Registered new member", f"Member ID: {member_id}"))
            print("Member registered successfully.")
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Register member failed", str(e)))
            print("Failed to register member.")

    def generate_member_id(self):
        """
        Generate a unique member ID with a checksum.
        """
        year = str(datetime.datetime.now().year)[-2:]
        random_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        checksum = str((sum(int(digit) for digit in (year + random_digits)) % 10))
        return year + random_digits + checksum

class GetMemberDetailsCommand(Command):
    def execute(self):
        """
        Execute the command to get member details.
        """
        try:
            member_id = self.get_validated_input("numeric", "Enter the member ID to retrieve details: ")
            member = _DBManager.select(
                "SELECT * FROM members WHERE member_id = ?", 
                (member_id,),
                encrypt_indexes=[1, 2, 3, 4, 5, 6, 7, 8, 9]
            )
            if member:
                print(member)
                _Logger.log_activity((_Authorizer.get_current_user()[1], "Retrieved member details", f"Member ID: {member_id}"))
            else:
                print("Member not found.")
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Get member details failed", str(e)))
            print("Failed to get member details.")

class DeleteMemberCommand(Command):
    def execute(self):
        """
        Execute the command to delete a member.
        """
        try:
            member_id = self.get_validated_input("numeric", "Enter the member ID to delete: ")
            _DBManager.modify("DELETE FROM members WHERE member_id = ?", (member_id,))
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Deleted member", f"Member ID: {member_id}"))
            print("Member deleted successfully.")
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Delete member failed", str(e)))
            print("Failed to delete member.")

class SearchMemberCommand(Command):
    def execute(self):
        """
        Execute the command to search for a member.
        """
        try:
            search_key = input("Enter search key (name, email, phone, etc.): ").lower()
            members = _DBManager.select_all("SELECT * FROM members", encrypt_indexes=[1, 2, 3, 4, 5, 6, 7, 8, 9])
            filtered_members = [
                member for member in members
                if search_key in member[1].lower() or # Firstname
                   search_key in member[2].lower() or # Lastname
                   search_key in member[7].lower() or # Email
                   search_key in member[8].lower() # Phone 
            ]
            for member in filtered_members:
                print(f"Member ID: {str(member[0])}, Firstname: {member[1]}, Lastname: {member[2]} Email: {member[7]} Phone: {member[8]}")
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Searched members", f"Search key: {search_key}"))
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Search members failed", str(e)))
            print("Failed to search members.")

class UpdateMemberCommand(Command):
    def execute(self):
        """
        Execute the command to update a member's information.
        """
        try:
            member_id = self.get_validated_input("numeric", "Enter the member ID to update: ")
            first_name = self.get_validated_input("name", "Enter the new first name of the member: ")
            last_name = self.get_validated_input("name", "Enter the new last name of the member: ")
            age = self.get_validated_input("numeric", "Enter the new age of the member: ")
            gender = self.get_validated_input("alpha", "Enter the new gender of the member: ")
            weight = self.get_validated_input("numeric", "Enter the new weight of the member: ")
            address = input("Enter the new address of the member: ")
            email = self.get_validated_input("email", "Enter the new email of the member: ")
            phone = self.get_validated_input("phone", "Enter the new phone number of the member: ")

            _DBManager.modify(
                "UPDATE members SET first_name = ?, last_name = ?, age = ?, gender = ?, weight = ?, address = ?, email = ?, phone = ? WHERE member_id = ?",
                (first_name, last_name, age, gender, weight, address, email, phone, member_id),
                encrypt_indexes=[0, 1, 2, 3, 4, 5, 6, 7]    
            )

            _Logger.log_activity((_Authorizer.get_current_user()[1], "Updated member", f"Member ID: {member_id}"))
            print("Member updated successfully.")
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Update member failed", str(e)))
            print("Failed to update member.")

class ChangeUserRoleCommand(Command):
    def execute(self):
        """
        Execute the command to change a user's role.
        """
        try:
            user_id = self.get_validated_input("numeric", "Enter the user ID to change role: ")
            new_role = self.get_validated_input("role", "Enter the new role for the user: ")
            _DBManager.modify("UPDATE users SET role = ? WHERE user_id = ?", (new_role, user_id))
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Changed user role", f"User ID: {user_id}, New Role: {new_role}"))
            print("User role changed successfully.")
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Change user role failed", str(e)))
            print("Failed to change user role.")

class CheckUnreadSuspiciousActivitiesCommand(Command):
    def execute(self):
        """
        Execute the command to check unread suspicious activities.
        """
        try:
            suspicious_logs = _DBManager.select_all("SELECT * FROM logs WHERE suspicious = 'Yes' AND read = 'No'")
            if suspicious_logs:
                print("Unread suspicious activities detected:")
                for log in suspicious_logs:
                    print(log)
            else:
                print("No unread suspicious activities.")
            _DBManager.modify("UPDATE logs SET read = 'Yes' WHERE suspicious = 'Yes' AND read = 'No'")
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Checked unread suspicious activities", ""))
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Check unread suspicious activities failed", str(e)))
            print("Failed to check unread suspicious activities.")

class RestoreSystemCommand(Command):
    def execute(self):
        """
        Execute the command to restore the system from a backup.
        """
        try:
            with zipfile.ZipFile('backup.zip', 'r') as backup_zip:
                backup_zip.extractall()

            os.replace('backup_uniquemeal.db', 'uniquemeal.db')
            #os.replace('backup_logs.db', 'logs.db')

            _Logger.log_activity((_Authorizer.get_current_user()[1], "Restored system", ""))
            print("System restored successfully.")
        except Exception as e:
            _Logger.log_activity((_Authorizer.get_current_user()[1], "Restore system failed", str(e)))
            print("Failed to restore system.")

class LogoutCommand(Command):
    def execute(self):
        """
        Execute the command to logout the current user.
        """
        print("Logout...")
        _Logger.log_activity((_Authorizer.get_current_user()[1], "User logged out", ""))
        _Authenticator.logout()

class UpdateOwnPasswordCommand(Command):
    def execute(self):
        """
        Execute the command to update the current user's password.
        """
        current_user = _Authorizer.get_current_user()
        if current_user:
            old_password = self.get_validated_input("password", "Enter your current password: ")
            new_password = self.get_validated_input("password", "Enter your new password: ")
            if _Authenticator.change_password(old_password, new_password):
                print("Password updated successfully.")
                _Logger.log_activity((current_user[1], "Updated own password", ""))
            else:
                print("Failed to update password. Please try again.")
                _Logger.log_activity((current_user[1], "Failed to update own password", ""))
        else:
            print("No user is currently logged in.")

# Register commands in the Factory
class CommandFactory:
    commands = {
        "list_users": CheckListOfUsersCommand(), 
        "add_consultant": AddUserCommand("Consultant"),
        "update_consultant": UpdateUserCommand(),
        "delete_consultant": DeleteUserCommand(),
        "reset_consultant_password": UpdateUserPasswordCommand(),
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
        """
        Get the command object based on the function name.
        """
        return CommandFactory.commands.get(function_name)
    
    def execute_function(self, function_name):
        """
        Execute the function based on the function name.
        """
        try:
            command = self.get_command(function_name)
            if command:
                command.execute()
                # Notify admin of unread suspicious activities after any command
                #if _Authorizer.get_current_role() in ["System Administrator", "Super Administrator"]:
                #    Logger.get_instance().check_unread_suspicious_activities()
            else:
                print("Invalid command. Please try again.")
                _Logger.log_activity((_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "Invalid command execution attempt", f"Function name: {function_name}"))
        except Exception as e:
            print(e)
            print("An unexpected error occurred while executing your command. Please try again.")
            _Logger.log_activity((_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "Exception occurred", str(e)))
