# store for UserData

class UserDataStore:
    def __init__(self):
        self.user_list = []

    def add(self, user_data):
        self.user_list.append(user_data)

    def find_by_username(self, username):
        for user in self.user_list:
            if user.username == username:
                return user
        return None
