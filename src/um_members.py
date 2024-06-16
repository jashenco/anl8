# ANL-8 SQ
# Reynethan Leon - 0959331
# Jasper van Gent - 0991834

from db import DBManager
from users import UserManager, Authorization, Authentication
from logging import Logger
from validation import InputValidator
from views import display_login, display_menu, display_header
from encryption import EncryptionManager
from mediator import EventHandler
from commands import CommandFactory

_EventHandler = EventHandler.get_instance()
_Logger = Logger.get_instance()
_DBManager = DBManager.get_instance()
_EncryptionManager = EncryptionManager(_EventHandler)
_Validator = InputValidator(_EventHandler, None)
_Authenticator = Authentication.get_instance(_DBManager, _EventHandler, _EncryptionManager, _Validator)
_Authorizer = Authorization.get_instance(_Authenticator)
_Validator = InputValidator(_EventHandler, _Authorizer)
_UserManager = UserManager(_EventHandler, _DBManager, _Validator)
_CommandFactory = CommandFactory()

def main():
    try:
        display_header()
        _EventHandler.emit("log_event", ("System", "Application Start", "System started"))

        display_login(_Authenticator, _Authorizer, _Validator, _EventHandler)

        role = _Authorizer.get_current_role()
        if role == "Super Administrator" or role == "System Administrator":
            _Logger.check_unread_suspicious_activities()

        if role:  # Only display menu if user is logged in
            _EventHandler.emit("log_event", ("User", "Login Successful", f"User with role {role} logged in"))
            display_menu(_Authenticator, _Authorizer, _Validator, _EventHandler, _CommandFactory)
        else:
            _EventHandler.emit("log_event", ("User", "Login Failed", "Unauthorized login attempt"))

    except Exception as e:
        _EventHandler.emit("log_event", ("System", "Main Application Error", str(e)))

    finally:
        # Ensure any necessary cleanup here
        _EventHandler.emit("log_event", ("System", "Application Shutdown", "System shutting down"))

if __name__ == "__main__":
    main()

