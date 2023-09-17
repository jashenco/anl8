import unittest
from admin import delete_user, change_user_role
from utils import user_exists, get_user_role

class TestAdmin(unittest.TestCase):

    def test_delete_user(self):
        # Assuming you have a function to check if a user exists
        delete_user("existing_username")
        self.assertFalse(user_exists("existing_username"))

    def test_change_user_role(self):
        # Assuming you have a function to get a user's role
        change_user_role("existing_username", "new_role")
        self.assertEqual(get_user_role("existing_username"), "new_role")

if __name__ == '__main__':
    unittest.main()
