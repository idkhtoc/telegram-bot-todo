from datetime import datetime

class Task:
    def __init__(self, tasks):
        self.tasks = tasks

    async def add_task(self, user_id, task_text, date):
        if not self.tasks.find_one({'user': user_id, 'text': task_text, 'date': date}):
            self.tasks.insert_one({
                'user': user_id,
                'text': task_text,
                'date': date,
                'done': False
            })

            return True
        else:
            return False
