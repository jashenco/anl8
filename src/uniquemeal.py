# ANL-8 SQ
# Reynethan Leon - 0959331
# Jasper van Gent - 0991834

from db import DBManager
from users import UserManager, Authorization, Authentication
from logging import Logger

from views import display_login, display_menu, display_header

_DBManager = DBManager.get_instance()
_UserManager = UserManager()
_Authenticator = Authentication.get_instance()
_Authorizer = Authorization.get_instance(_Authenticator)
_Logger = Logger.get_instance()

def main():
    try:
        display_header()
        _Logger.log_activity("System", "Application Start", "System started")

        display_login()
        
        role = _Authorizer.get_current_role()
        if role:  # Only display menu if user is logged in
            _Logger.log_activity("User", "Login Successful", f"User with role {role} logged in")
            display_menu()
        else:
            _Logger.log_activity("User", "Login Failed", "Unauthorized login attempt")

    except Exception as e:
        _Logger.log_activity("System", "Main Application Error", str(e))

    finally:
        # Ensure any necessary cleanup here
        _Logger.log_activity("System", "Application Shutdown", "System shutting down")

if __name__ == "__main__":
    main()
