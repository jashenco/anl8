import re

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
    def __init__(self, event_handler, authorizer):
        """
        Initialize InputValidator with predefined regex patterns for different input types.
        """
        self._EventHandler = event_handler
        self._Authorizer = authorizer
        # Whitelist patterns for different input types
        self.patterns = {
            "alpha": r"^[a-zA-Z]+$",  # Only letters
            "alphanumeric": r"^[a-zA-Z0-9]+$",  # Letters and numbers
            "numeric": r"^[0-9]+$",  # Only numbers
            "username": r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,11}$",  # Username format: 8-10 characters, starts with letter or underscore
            "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&\_\-+=`|\\(){}[\]:;'<>,.?/])[A-Za-z\d~!@#$%&\_\-+=`|\\(){}[\]:;'<>,.?/]{12,30}$",  # Password format: 12-30 characters, at least one lowercase, one uppercase, one digit, one special character
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",  # Email format
            "phone": r"^\d{8}$",  # Mobile phone format: 8 digits
            "url": r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$",  # URL format
            "role": r"(Super Administrator|System Administrator|Consultant)",  # Role: predefined roles
            "name": r"^[a-zA-Z]+(?:[-' .][a-zA-Z]+)*$",  # Name format: letters with optional separators
            "zip_code": r"^\d{4}[A-Z]{2}$",  # Zip code format: 4 digits followed by 2 uppercase letters
            "address": r"^[\w\s,-]+$",  # Address format: simplistic validation for street name and house number
        }
        # Predefined list of cities
        self.cities = ["Amsterdam", "Rotterdam", "Utrecht", "Eindhoven", "Groningen", "Haarlem", "Leiden", "Maastricht", "Nijmegen", "Arnhem"]
        
    def validate(self, input_type, data):
        """
        Validate the data based on the input type using regex patterns and specific checks.
        """
        try:
            # Check for specific non-regex exceptions
            if input_type == "username" and data == 'super_admin':
                return True
            if input_type == "password" and data == 'Admin_123!':
                return True
            if (input_type == "username" and data == "exit") or (input_type == "password" and data == "exit"):
                return True
            if input_type == "numeric" and data == "exit":
                return True

            # Validate city from predefined list
            if input_type == "address":
                if data in self.cities:
                    return data
                else:
                    error_message = "Not a supported city. Supported cities are: " + ' '.join(self.cities)
                    self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._Authorizer.get_current_user() else "System", "Invalid city", f"City: {data}"))
                    raise ValidationError(error_message)

            # Check for unknown input type
            if input_type not in self.patterns:
                self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._Authorizer.get_current_user() else "System", "Invalid input type", f"Input type: {input_type}"))
                raise ValidationError("Unknown input type", context={"input_type": input_type})
            
            # NULL byte check
            if self._contains_null_byte(data):
                self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._Authorizer.get_current_user() else "System", "NULL byte detected", f"Data: {data}"))
                raise ValidationError("Data contains NULL byte", context={"data": data})
            
            # SQL Injection check
            if self._is_sql_injection(data):
                self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._Authorizer.get_current_user() else "System", "SQL Injection detected", f"Data: {data}", 'Yes'))
                raise ValidationError("Data contains SQL Injection pattern", context={"data": data})

            # Regex validation
            pattern = self.patterns[input_type]
            if re.match(pattern, data):
                return True
            else:
                self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._Authorizer.get_current_user() else "System", "Invalid input", f"Input type: {input_type}, Data: {data}"))
                raise ValidationError(f"Invalid {input_type} format")
        
        except ValidationError as e:
            self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._Authorizer.get_current_user() else "System", "Validation Exception", str(e)))
            print("Invalid input. Please try again.")
            print(e)
            return False
        except Exception as e:
            self._EventHandler.emit("log_event", (self._Authorizer.get_current_user()[1] if self._Authorizer.get_current_user() else "System", "General Exception", str(e)))
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
        Check for common SQL Injection patterns using regex.
        """
        patterns = [
            r"(?i)UNION(?:\s+ALL)?\s+SELECT",  # UNION SELECT
            r"(?i)SELECT\s+\*",  # SELECT *
            r"(?i)DROP\s+TABLE",  # DROP TABLE
            r"(?i)OR\s+1\s*=\s*1",  # OR 1=1
            r"(?i)AND\s+1\s*=\s*0",  # AND 1=0
            r"(?i)INSERT\s+INTO",  # INSERT INTO
            r"(?i)DELETE\s+FROM",  # DELETE FROM
            r"(?i)UPDATE\s+\w+\s+SET",  # UPDATE ... SET
            r"(?i)CREATE\s+TABLE",  # CREATE TABLE
            r"(?i)ALTER\s+TABLE",  # ALTER TABLE
            r"(?i)EXEC(\s+\w+)?",  # EXEC
            r"(?i)DECLARE\s+\w+\s+AS",  # DECLARE ... AS
            r"(?i)WAITFOR\s+DELAY",  # WAITFOR DELAY
            r"(?i)--\s+",  # SQL comment --
            r"(?i)\/\*[\w\W]*\*\/",  # SQL comment /* */
            r"(?i);[^\s]",  # SQL injection using ;
            r"(?i)xp_cmdshell",  # xp_cmdshell
            r"(?i)DBCC",  # DBCC
            r"(?i)HAVING\s+1\s*=\s*1",  # HAVING 1=1
            r"(?i)LOAD_FILE",  # LOAD_FILE
            r"(?i)INTO\s+OUTFILE",  # INTO OUTFILE
            r"(?i)DUMPFILE",  # DUMPFILE
            r"(?i)FROM\s+INFORMATION_SCHEMA",  # FROM INFORMATION_SCHEMA
            r"(?i)LIKE\s+binary"  # LIKE binary
        ]
        
        for pattern in patterns:
            if re.search(pattern, data):
                return True
        return False
