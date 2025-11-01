import unittest
import user_data

class TestUserData(unittest.TestCase):
    def test_init_get(self):
        freddy = user_data.UserData('freddy', 'Test123', 1)
        self.assertEqual(freddy.username, 'freddy')
        self.assertEqual(freddy.password, 'Test123')
        self.assertEqual(freddy.account_number, 1)

if __name__ == '__main__':
    unittest.main()
