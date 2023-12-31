from users import Authentication, Authorization
from commands import CommandFactory
from validation import InputValidator
from logging import Logger

_Authenticator = Authentication.get_instance()
_Authorizer = Authorization.get_instance(_Authenticator)

_CommandFactory = CommandFactory()

_Validator = InputValidator()

_Logger = Logger.get_instance()

def display_header():
    print("=======================================")
    print("            FitPlus System             ")
    print("=======================================")
    print("\nWelcome to FitPlus! Please login to continue.\n")

def display_login():
    username = _Validator.validate("username", input("Enter username: "))
    password = _Validator.validate("password", input("Enter password: ")) 

    if not username or not password:
        print("Invalid username or password input. Try again.")
        display_login()

    success = _Authenticator.login(username, password)

    if success:
        print(f"Welcome, {username}! You are logged in as {_Authorizer.get_current_role()}.")

    else:
        print("Login failed. Try again.")
        display_login()

def display_menu():
    current_role = _Authorizer.get_current_role()
    print(f"\n{current_role} Menu:\n")
    
    role_options = _Authorizer.get_role_options()
    
    for key, value in role_options.items():
        print(f"{key}. {value['description']}")
    
    while True:
        try:
            choice = _Validator.validate("numeric", input("\nPlease enter the number corresponding to your choice (or 'exit' to exit): "))
            if choice == "exit":
                break
            if choice in role_options:
                function_name = role_options[choice]['function']
                _CommandFactory.execute_function(function_name)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print("An unexpected error occurred while executing your command. Please try again.")
            _Logger.log_activity(_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "Exception occurred", str(e))
