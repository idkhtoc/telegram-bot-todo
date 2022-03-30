import asyncio
from datetime import datetime
from pymongo import MongoClient
from aiogram import types

client = MongoClient()
users = client['Users']


class TasksSend:
    def __init__(self, user):
        self.user = users[str(user.id)]

    async def send(self, message, date):
        tasks = list(self.user.find({'date': str(date)}))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Добавить задание').row('Все задания', 'Все задания за дату:')

        if tasks:
            text = f'Все задания на {date}'

            await message.answer(text, reply_markup=markup)

            for i, el in enumerate(tasks):
                text = f'{"✅"*14 if el["done"] else "❌"*14}\n\n{el["text"]}'

                if date == datetime.now().date():
                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton('Изменить', callback_data='done')) \
                          .add(types.InlineKeyboardButton('Удалить', callback_data='delete'))

                    await message.answer(text, reply_markup=markup)
                else:
                    await message.answer(text)

        else:
            await message.answer('Заданий нет(', reply_markup=markup)
