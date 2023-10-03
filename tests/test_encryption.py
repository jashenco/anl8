import unittest
from encryption import encrypt_data, decrypt_data

class TestEncryption(unittest.TestCase):

    def test_encrypt_decrypt(self):
        original_data = "This is a test string."
        
        # Test encryption
        encrypted_data = encrypt_data(original_data)
        self.assertNotEqual(encrypted_data, original_data)
        
        # Test decryption
        decrypted_data = decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, original_data)

if __name__ == "__main__":
    unittest.main()
