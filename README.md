# Fit+ System

# Setup

- Create virtual env (to keep all dependencies for project seperated) (*differs for mac (install virtualenv with sudo pip ...) / linux*).   
```virtualenv venv``` (use python 3.9 using ```--python 3.9```)
```python3 -m venv venv```

- Activate Virtual Environment
```.\venv\Script\activate```
Or on Mac OS / Linux:
```source venv/bin/activate```

- Install Dependecies
```pip install -r requirements.txt```

- Run main script
```py main.py``` or ```python3 main.py```

# Working together

- When adding dependencies
```pip freeze > requirements.txt```

- Work as much OPP as possible. Use classes and design patterns to assure quality.

# User Guide

## Encryption in Fit+ Application

### Key Management
The application generates a pair of public and private keys for encryption and decryption. These keys are stored in the project directory as `private_key.pem` and `public_key.pem`.

### Data Encryption and Decryption
All sensitive data, like addresses, emails, and phone numbers, are encrypted using an asymmetric encryption algorithm before being stored in the database. When reading from the database, the data is decrypted on-the-fly within the application.

### Important Note for Grading
The encryption keys are included in the project directory. Please do not move or delete these files for the application to function correctly during grading.

### Security Compliance
The encryption and decryption process complies with the assignment's "Additional Clarification," ensuring that data is not readable outside of the application.
