from datetime import datetime

from modules.keyboards import task_inline_keyboard

class TaskButtons:
    def __init__(self, tasks):
        self.tasks = tasks;

    async def delete(self, user_id, text, date):
        successful = self.tasks.find_one_and_delete({'user': user_id, 'text': text[16:], 'date': date})

        return bool(successful)

    async def done(self, user_id, message_text, date):
        task_text = message_text.replace('✅', '').replace('❌', '').strip()

        task = self.tasks.find_one({'user': user_id, 'text': task_text, 'date': date})
        
        self.tasks.find_one_and_update({'user': user_id, 'text': task_text, 'date': date},
                                      {'$set': {'done': not task['done']}})
        
        text = ''

        if task['done']:
            text = message_text.replace('✅', '❌')
        else:
            text = message_text.replace('❌', '✅')

        markup = task_inline_keyboard()

        return text, markup
