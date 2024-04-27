class Registration:
    def __init__(self, users):
        self.users = users

    async def add(self, user_id, user_name):

        if not self.users.find_one({'_id': str(user_id)}):
            self.users.insert_one({'_id': str(user_id), 'name': user_name })
