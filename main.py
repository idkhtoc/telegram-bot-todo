import asyncio
from datetime import datetime
import logging
import json
from pymongo import MongoClient
from aiogram import Bot, types, Dispatcher, executor, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from modules.task import Task
from modules.tasks_send import TasksSend
from modules.task_buttons import TaskButtons
from modules.registration import Register
from modules.states import States

with open('C:\Programming\Python\TelegramBotToDoList\CONFIG.json', 'r') as json_file:
    token = json.load(json_file)['API_TOKEN']

logging.basicConfig(level=logging.INFO)
myBot = Bot(token=token)
dp = Dispatcher(myBot, storage=MemoryStorage())

client = MongoClient()
start_texts = client['Texts']['StartTexts']

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('Добавить задание').row('Все задания', 'Все задания за дату:')


@dp.message_handler(commands=['start', 'help'])
async def command(message: types.Message):
    if message.text == '/start':
        await Register(message.from_user).add()

        start_text = start_texts.find_one({'type': 'start'})['text']

        await message.answer(start_text, reply_markup=markup)


@dp.message_handler(filters.Text(equals=['Добавить задание', 'Все задания', 'Все задания за дату:']))
async def add_new_task(message: types.Message):
    if message.text == 'Добавить задание':
        add_text = start_texts.find_one({'type': 'addTask'})['text']

        await message.answer(add_text, reply_markup=types.ReplyKeyboardRemove())

        await States.new_task_state.set()

    elif message.text == 'Все задания':
        await TasksSend(message.from_user).send(message, datetime.now().date())

    elif message.text == 'Все задания за дату:':
        date_text = start_texts.find_one({'type': 'dateTasks'})['text']

        await message.answer(date_text, reply_markup=types.ReplyKeyboardRemove())

        await States.time_state.set()


@dp.message_handler(content_types=['text'], state=States.new_task_state)
async def task_text(message: types.Message, state: FSMContext):
    await state.finish()

    if message.text:
        task = await Task(message.text, message.from_user).add_task()

        if task:
            text = start_texts.find_one({'type': 'addSuccessfully'})['text']
        else:
            text = start_texts.find_one({'type': 'addBadly'})['text']

        await message.answer(text, reply_markup=markup)


@dp.message_handler(content_types=['text'], state=States.time_state)
async def date_text(message: types.Message, state: FSMContext):
    await state.finish()

    try:
        date = datetime.strptime(message.text, '%d.%m.%Y').date()
        await TasksSend(message.from_user).send(message, date)
    except:
        await message.answer('Вы неправильно ввели дату(', reply_markup=markup)


@dp.callback_query_handler(lambda call: True)
async def task_buttons(call):
    if call.data == 'delete':
        await TaskButtons(call).delete()

    elif call.data == 'done':
        await TaskButtons(call).done(myBot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
