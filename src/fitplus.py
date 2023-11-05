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
        display_login()

        if _Authorizer.get_current_role(): # Only display menu if user is logged in
            display_menu()

    except Exception as e:
        _Logger.log_activity("System", "Main Apllication Error", str(e))

if __name__ == "__main__":
    main()
