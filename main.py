import asyncio
from datetime import datetime
import logging
import json
import sys
from pymongo import MongoClient
from aiogram import Bot, types, Dispatcher, filters, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext


from modules.task import Task
from modules.tasks_send import TasksSend
from modules.task_buttons import TaskButtons
from modules.registration import Registration
from modules.states import States
from modules.keyboards import main_keyboard

import constants as constants

with open('./CONFIG.json', 'r') as json_file:
    config = json.load(json_file)

    token = config['API_TOKEN']
    client = MongoClient(config['DB_URL'])
    db = client[config['DB_NAME']]

router = Router()
myBot = Bot(token)

markup = main_keyboard()

task_buttons = TaskButtons(db.tasks)
registration = Registration(db.users)
states = States()
task = Task(db.tasks)
tasks_send = TasksSend(db.tasks)

@router.message(filters.Command(commands=['start', 'help']))
async def command(message: types.Message):
    if message.text == '/start':
        await registration.add(message.from_user.id, message.from_user.username)

        await message.answer(constants.START_TEXT, reply_markup=markup)


@router.message(F.text.in_(constants.NOTES_TEXTS))
async def add_new_task(message: types.Message, state: FSMContext):
    if message.text == constants.ADD_TASK_TEXT:
        await message.answer(constants.ADD_TEXT, reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(states.new_task_state)

    elif message.text == constants.ALL_NOTES_TEXT:
        await tasks_send.send(message, str(message.date.date()))

    elif message.text == constants.ALL_NOTES_TEXT_DATE:
        await message.answer(constants.DATE_NOTES_TEXT, reply_markup=types.ReplyKeyboardRemove())

        await state.set_state(states.time_state)


@router.message(F.text and states.new_task_state)
async def task_text(message: types.Message, state: FSMContext):
    await state.clear()

    if message.text:
        answer = constants.ADD_BADLY_TEXT

        if await task.add_task(message.from_user.id, message.text, str(message.date.date())):
            answer = constants.ADD_SUCCESSFULY_TEXT

        await message.answer(answer, reply_markup=markup)


@router.message(F.text and states.time_state)
async def date_text(message: types.Message, state: FSMContext):
    await state.clear()

    try:
        date = datetime.strptime(message.text, '%d.%m.%Y').date()
        await tasks_send.send(message, str(date))
    except:
        await message.answer(constants.FALSE_DATE_TEXT, reply_markup=markup)


@router.callback_query(F.data)
async def task_buttons_handler(call):
    if call.data == 'delete':
        if await task_buttons.delete(call.from_user.id, call.message.text, str(call.message.date.date())):
            await call.message.delete()

    elif call.data == 'done':
        text, markup = await task_buttons.done(call.from_user.id, call.message.text, str(call.message.date.date()))

        await myBot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await dp.start_polling(myBot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
