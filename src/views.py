from users import Authentication, Authorization
from commands import CommandFactory
from validation import InputValidator
from logging import Logger
from mediator import EventHandler

_Authenticator = Authentication.get_instance()
_Authorizer = Authorization.get_instance(_Authenticator)
_CommandFactory = CommandFactory()
_Validator = InputValidator()
_EventHandler = EventHandler.get_instance()

def display_header():
    print("=======================================")
    print("            Unique Meal System         ")
    print("=======================================")
    print("\nWelcome to Unique Meal! Please login to continue.\n")

def display_login():
    print("Login\n")
    username = _Validator.validate("username", input("Enter username: "))
    password = _Validator.validate("password", input("Enter password: "))
    print("\nSuccess!\n") 

    if not username or not password:
        print("Invalid username or password input. Try again.\n")
        _EventHandler.emit("log_event", ("System", "Invalid Input", "Invalid username or password input."))
        display_login()

    print(f"Attempting to log in as {username}...")
    success = _Authenticator.login(username, password)
    print(f"Success: {success}")

    if success:
        _EventHandler.emit("log_event", (username, "Login Successful", f"User {username} logged in as {_Authorizer.get_current_role()}."))
        print(f"Welcome, {username}! You are logged in as {_Authorizer.get_current_role()}.")
    else:
        _EventHandler.emit("log_event", (username, "Login Failed", "Login attempt failed."))
        print("Login failed. Try again.\n")
        display_login()

def display_menu():
    current_role = _Authorizer.get_current_role()
    print(f"\n{current_role} Menu:\n")
    
    role_options = _Authorizer.get_role_options()
    
    for key, value in role_options.items():
        print(f"{key}. {value['description']}")
    
    while True:
        try:
            choice = input("\nPlease enter the number corresponding to your choice (or 'exit' to exit): ")
            if choice == "exit":
                break
            choice = _Validator.validate("numeric", choice)
            if choice in role_options:
                function_name = role_options[choice]['function']
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1], "Menu Selection", f"Selected option: {choice} - {function_name}"))
                _CommandFactory.execute_function(function_name)
            else:
                print("Invalid choice. Please try again.")
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1], "Invalid Menu Selection", f"Invalid choice entered: {choice}"))
        except Exception as e:
            print("An unexpected error occurred while executing your command. Please try again.")
            _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1], "Command Execution Error", str(e)))

