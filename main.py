import asyncio
import logging
import json
from pymongo import MongoClient
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from modules.registration import Register
from modules.states import States

with open('C:\Programming\Python\TelegramBotToDoList\CONFIG.json', 'r') as json_file:
    token = json.load(json_file)['API_TOKEN']

logging.basicConfig(level=logging.INFO)
myBot = Bot(token=token)
dp = Dispatcher(myBot, storage=MemoryStorage())

client = MongoClient()
start_texts = client['Texts']['StartTexts']


@dp.message_handler(commands=['start', 'help'])
async def command(message: types.Message):
    if message.text == '/start':
        await Register(message.from_user).add()

        start_text = start_texts.find_one({'command': 'start'})['text']

        await message.answer(start_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
