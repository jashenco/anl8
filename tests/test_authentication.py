import unittest
from authentication import login_user

class TestAuthentication(unittest.TestCase):

    def test_successful_login(self):
        self.assertTrue(login_user("existing_username", "correct_password"))

    def test_unsuccessful_login(self):
        self.assertFalse(login_user("existing_username", "wrong_password"))
        self.assertFalse(login_user("non_existing_username", "any_password"))

if __name__ == '__main__':
    unittest.main()
