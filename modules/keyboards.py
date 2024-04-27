from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import constants

def main_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text=constants.ADD_TASK_TEXT)],
        [KeyboardButton(text=constants.ALL_NOTES_TEXT), KeyboardButton(text=constants.ALL_NOTES_TEXT_DATE)]
    ])

def task_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=constants.CHANGE_TEXT, callback_data='done'),
        InlineKeyboardButton(text=constants.DELETE_TEXT, callback_data='delete')
    ]])