import asyncio
from pymongo import MongoClient
from datetime import datetime
from aiogram import types

client = MongoClient()
users = client['Users']


class TaskButtons:
    def __init__(self, call):
        self.user = users[str(call.from_user.id)]
        self.message = call.message
        self.text = call.message.text[16:]

    async def delete(self):
        self.user.find_one_and_delete({'text': self.text, 'date': str(datetime.now().date())})
        await self.message.delete()

    async def done(self, bot):
        task = self.user.find_one({'text': self.text, 'date': str(datetime.now().date())})
        self.user.find_one_and_update({'text': self.text, 'date': str(datetime.now().date())},
                                      {'$set': {'done': not task['done']}})
        if task['done']:
            text = self.message.text.replace('✅', '❌')
        else:
            text = self.message.text.replace('❌', '✅')

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Изменить', callback_data='done')) \
              .add(types.InlineKeyboardButton('Удалить', callback_data='delete'))

        await bot.edit_message_text(text, self.message.chat.id, self.message.message_id, reply_markup=markup)
