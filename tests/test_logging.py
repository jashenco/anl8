import unittest
from logging import log_activity, flag_suspicious_activity
from utils import activity_logged

class TestLogging(unittest.TestCase):

    def test_log_activity(self):
        # Assuming you have a function to check if an activity is logged
        log_activity("username", "description", "additional_info", "No")
        self.assertTrue(activity_logged("username", "description"))

    def test_flag_suspicious_activity(self):
        self.assertEqual(flag_suspicious_activity("username", "Unsuccessful login"), "No")
        self.assertEqual(flag_suspicious_activity("username", "Unsuccessful login"), "No")
        self.assertEqual(flag_suspicious_activity("username", "Unsuccessful login"), "Yes")

if __name__ == '__main__':
    unittest.main()
