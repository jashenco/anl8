#User Guide

## Encryption in Fit+ Application

### Key Management
The application generates a pair of public and private keys for encryption and decryption. These keys are stored in the project directory as `private_key.pem` and `public_key.pem`.

### Data Encryption and Decryption
All sensitive data, like addresses, emails, and phone numbers, are encrypted using an asymmetric encryption algorithm before being stored in the database. When reading from the database, the data is decrypted on-the-fly within the application.

### Important Note for Grading
The encryption keys are included in the project directory. Please do not move or delete these files for the application to function correctly during grading.

### Security Compliance
The encryption and decryption process complies with the assignment's "Additional Clarification," ensuring that data is not readable outside of the application.