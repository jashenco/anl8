# ANL-8 SQ
# Reynethan Leon - 0959331
# Jasper van Gent - 0991834

from db import DBManager
from users import UserManager, Authorization, Authentication
from logging import Logger

from views import display_login, display_menu, display_header

from mediator import EventHandler

_EventHandler = EventHandler()
_Logger = Logger.get_instance()
_DBManager = DBManager.get_instance()
_UserManager = UserManager()
_Authenticator = Authentication.get_instance()
_Authorizer = Authorization.get_instance(_Authenticator)

def main():
    try:
        display_header()
        _EventHandler.emit("log_event", ("System", "Application Start", "System started"))

        display_login()
        
        print("login successful")
        role = _Authorizer.get_current_role()
        print("Role established")

        if role:  # Only display menu if user is logged in
            _EventHandler.emit("log_event", ("User", "Login Successful", f"User with role {role} logged in"))
            display_menu()
        else:
            _EventHandler.emit("log_event", ("User", "Login Failed", "Unauthorized login attempt"))

    except Exception as e:
        _EventHandler.emit("log_event", ("System", "Main Application Error", str(e)))

    finally:
        # Ensure any necessary cleanup here
        _EventHandler.emit("log_event", ("System", "Application Shutdown", "System shutting down"))

if __name__ == "__main__":
    main()
