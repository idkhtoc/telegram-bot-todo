import asyncio
from datetime import datetime
from pymongo import MongoClient

client = MongoClient()
users = client['Users']


class Task:
    def __init__(self, text, user):
        self.task_text = text
        self.user = users[str(user.id)]

    async def add_task(self):
        if not self.user.find_one({'text': self.task_text, 'date': str(datetime.now().date())}):
            self.user.insert_one({
                'text': self.task_text,
                'date': str(datetime.now().date()),
                'done': False
            })

            return True
        else:
            return False
