from users import Authorization, Authentication
import re
from mediator import EventHandler

_EventHandler = EventHandler.get_instance()
_Authenticator = Authentication.get_instance()
_Authorizer = Authorization.get_instance(_Authenticator)

class ValidationError(Exception):
    def __init__(self, message, context=None):
        """
        Initialize ValidationError with an error message and optional context.
        """
        super().__init__(message) 
        self.context = context if context else {}

    def __str__(self):
        """
        Return the error message. If context is provided, append it to the message.
        """
        base_msg = super().__str__()
        if self.context:
            context_msg = ", ".join(f"{key}: {value}" for key, value in self.context.items())
            return f"{base_msg} (Context: {context_msg})"
        return base_msg

class InputValidator:
    def __init__(self):
        # Whitelist patterns for different input types
        self.patterns = {
            "alpha": r"^[a-zA-Z]+$",
            "alphanumeric": r"^[a-zA-Z0-9]+$",
            "numeric": r"^[0-9]+$",
            "username": r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,11}$",
            "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&\_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&\_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$",
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "phone": r"^\+?\d{10,15}$",
            "url": r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$",
            "role": r"(Super Administrator|System Administrator|Consultant)",
            "name": r"^[a-zA-Z]+(?:[-' .][a-zA-Z]+)*$"
        }
        
    def validate(self, input_type, data):
        """
        Validate the data based on the input type.
        """
        try:
            # Check for specific non-regex exceptions
            if input_type == "username" and data == 'super_admin':
                return data
            if input_type == "password" and data == 'Admin_123!':
                return data
            if (input_type == "username" and data == "exit") or (input_type == "password" and data == "exit"):
                return data
            
            if input_type == "numeric" and data == "exit":
                return data

            if input_type not in self.patterns:
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "Invalid input type", f"Input type: {input_type}"))
                raise ValidationError("Unknown input type", context={"input_type": input_type})
            
            # NULL byte check by regex
            if self._contains_null_byte(data):
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "NULL byte detected", f"Data: {data}"))
                raise ValidationError("Data contains NULL byte", context={"data": data})
            
            # SQL Injection check by regex
            if self._is_sql_injection(data):
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "SQL Injection detected", f"Data: {data}"))
                raise ValidationError("Data contains SQL Injection pattern", context={"data": data})
            
            #print(f"Validating {input_type}: {data}")

            pattern = self.patterns[input_type]
            if re.match(pattern, data):
                return data
            else:
                print(f"Invalid input. Try again.")
                _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "Invalid input", f"Input type: {input_type}, Data: {data}"))
                return False
            
        except ValidationError as e:
            _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "Validation Exception", str(e)))
            print("Invalid input. Please try again.")
            return False
        except Exception as e:
            _EventHandler.emit("log_event", (_Authorizer.get_current_user()[1] if _Authorizer.get_current_user() else "System", "General Exception", str(e)))
            print("Invalid input. Please try again.")
            print(e)
            return False
        
    def _contains_null_byte(self, data):
        """
        Check if data contains NULL byte.
        """
        return "\0" in data
        
    def _is_sql_injection(self, data):
        """
        Check for common SQL Injection patterns.
        """
        patterns = [
            r"(?i)UNION(?:\s+ALL)?\s+SELECT",
            r"(?i)SELECT\s+\*",
            r"(?i)DROP\s+TABLE",
            r"(?i)OR\s+1\s*=\s*1",
            r"(?i)AND\s+1\s*=\s*0",
            r"(?i)INSERT\s+INTO",
            r"(?i)DELETE\s+FROM",
            r"(?i)UPDATE\s+\w+\s+SET",
            r"(?i)CREATE\s+TABLE",
            r"(?i)ALTER\s+TABLE",
            r"(?i)EXEC(\s+\w+)?",
            r"(?i)DECLARE\s+\w+\s+AS",
            r"(?i)WAITFOR\s+DELAY",
            r"(?i)--\s+",
            r"(?i)\/\*[\w\W]*\*\/",
            r"(?i);[^\s]", 
            r"(?i)xp_cmdshell",
            r"(?i)DBCC",
            r"(?i)HAVING\s+1\s*=\s*1",
            r"(?i)LOAD_FILE",
            r"(?i)INTO\s+OUTFILE",
            r"(?i)DUMPFILE",
            r"(?i)FROM\s+INFORMATION_SCHEMA",
            r"(?i)LIKE\s+binary"
        ]
        
        for pattern in patterns:
            if re.search(pattern, data):
                return True
        return False
