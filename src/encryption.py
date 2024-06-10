from cryptography.hazmat.primitives import serialization, asymmetric, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import os

class EncryptionManager:
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.private_key_path = "private_key.pem"
        self.public_key_path = "public_key.pem"
        self.private_key = None
        self.public_key = None
        self.load_or_generate_keys()

    def load_or_generate_keys(self):
        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            self.generate_keys()
        else:
            self.load_keys()

    def generate_keys(self):
        try:
            private_key = asymmetric.rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()

            # Serialize and save keys
            with open(self.private_key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            with open(self.public_key_path, "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
            self.private_key = private_key
            self.public_key = public_key
            
            self.event_handler.emit("log_event", ("System", "Key Generation", "Encryption keys generated and saved"))
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Key Generation Error", str(e)))

    def load_keys(self):
        try:
            with open(self.private_key_path, "rb") as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )

            with open(self.public_key_path, "rb") as f:
                self.public_key = serialization.load_pem_public_key(
                    f.read(),
                    backend=default_backend()
                )
            self.event_handler.emit("log_event", ("System", "Key Loading", "Encryption keys loaded"))
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Key Loading Error", str(e)))

    def encrypt_data(self, data):
        try:
            ciphertext = self.public_key.encrypt(
                data.encode('utf-8'),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return ciphertext
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Encryption Error", str(e)))
            return None

    def decrypt_data(self, ciphertext):
        try:
            plaintext = self.private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return plaintext.decode('utf-8')
        except Exception as e:
            self.event_handler.emit("log_event", ("System", "Decryption Error", str(e)))
            return None
