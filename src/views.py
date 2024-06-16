# views.py
from commands import CommandFactory

def display_header():
    print("=======================================")
    print("            Unique Meal System         ")
    print("=======================================")
    print("\nWelcome to Unique Meal! Please login to continue.\n")

def display_login(_Authenticator, _Authorizer, _Validator, _EventHandler):
    while True:
        username = _Validator.validate("username", input("Enter username: "))
        if username == "exit":
            print("Exiting...")
            return
        if not username:
            _EventHandler.emit("log_event", ("System", "Invalid Input", "Invalid username input."))
            continue

        password = _Validator.validate("password", input("Enter password: "))
        if password == "exit":
            print("Exiting...")
            return
        if not password:
            _EventHandler.emit("log_event", ("System", "Invalid Input", "Invalid password input."))
            continue

        # Authenticate user
        success = _Authenticator.login(username, password)

        if success:
            current_user = _Authorizer.get_current_role()
            _EventHandler.emit("log_event", (username, "Login Successful", f"User {username} logged in as {_Authorizer.get_current_role()}."))
            print(f"Welcome, {username}! You are logged in as {_Authorizer.get_current_role()}.")
            return
        else:
            _EventHandler.emit("log_event", (username, "Login Failed", "Login attempt failed."))
            print("Login failed. Try again.\n")



def display_menu(_Authenticator, _Authorizer, _Validator, _EventHandler, _CommandFactory):
    while True:
        current_role = _Authorizer.get_current_role()
        if not current_role:
            print("You are not logged in. Please login to continue.")
            display_login(_Authenticator, _Authorizer, _Validator, _EventHandler)
            continue

        print(f"\n{current_role} Menu:\n")

        role_options = _Authorizer.get_role_options()

        for key, value in role_options.items():
            print(f"{key}. {value['description']}")

        try:
            choice = input("\nPlease enter the number corresponding to your choice (or 'exit' to exit): ")
            if choice == "exit":
                break
            choice = _Validator.validate("numeric", choice)
            if choice in role_options:
                function_name = role_options[choice]['function']
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1], "Menu Selection", f"Selected option: {choice} - {function_name}"))
                _CommandFactory.execute_function(function_name)
                if function_name == "logout":
                    print("You have been logged out.")
                    break
                elif function_name == "restore_system":
                    print("System restored successfully.")
            else:
                print("Invalid choice. Please try again.")
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1], "Invalid Menu Selection", f"Invalid choice entered: {choice}"))
        except Exception as e:
            print("An unexpected error occurred while executing your command. Please try again.")
            _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1], "Command Execution Error", str(e)))