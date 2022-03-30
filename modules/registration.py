import asyncio
from pymongo import MongoClient

client = MongoClient()
users = client['Users']


class Register:
    def __init__(self, user):
        self.user_id = user.id

    async def add(self):
        if not str(self.user_id) in users.list_collection_names():
            await users.create_collection(str(self.user_id))
