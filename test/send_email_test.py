import unittest
from src.send_email import login_to_email


class MyTestCase(unittest.TestCase):
    def test_something(self):
        login_to_email()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
