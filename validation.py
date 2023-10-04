import re

class InputValidator:
    def __init__(self):
        # Whitelist patterns for different input types
        self.patterns = {
            "alpha": r"^[a-zA-Z]+$",
            "alphanumeric": r"^[a-zA-Z0-9]+$",
            "numeric": r"^[0-9]+$",
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "phone": r"^\+?\d{10,15}$",
            "url": r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$"  
        }
        
    def validate(self, input_type, data):
        """
        Validate the data based on the input type.
        """
        if input_type not in self.patterns:
            raise ValidationError(f"Unknown input type: {input_type}")
        
        pattern = self.patterns[input_type]
        if re.match(pattern, data):
            return True
        
        return False