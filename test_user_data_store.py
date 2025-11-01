import unittest
import user_data
import user_data_store

class TestUserDataStore(unittest.TestCase):
    def test_find_in_empty_store(self):
        store = user_data_store.UserDataStore()
        freddy = store.find_by_username('freddy')
        self.assertIsNone(freddy)

    def test_add_find_user(self):
        store = user_data_store.UserDataStore()
        user = user_data.UserData('freddy', 'Test123', 1)
        store.add(user)
        freddy = store.find_by_username('freddy')
        self.assertEqual(freddy.username, 'freddy')

if __name__ == '__main__':
    unittest.main()
